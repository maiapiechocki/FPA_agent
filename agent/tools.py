import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FinancialTools:
    """A collection of functions to perform financial analysis on the data."""

    def __init__(self, data_frames):
        self.data = self._prepare_data(data_frames)

    def _prepare_data(self, data_frames):
        """
        Pre-processes the raw dataframes. This is the most critical step.
        It converts all financial values to USD so they can be aggregated correctly.
        """
        actuals = data_frames['actuals'].copy().rename(columns={'account_category': 'account_c', 'amount': 'value'})
        budget = data_frames['budget'].copy().rename(columns={'account_category': 'account_c', 'amount': 'value'})
        cash = data_frames['cash'].copy().rename(columns={'cash_usd': 'cash_balance'})
        fx = data_frames['fx'].copy()

        # clean whitespace from currency columns for valid merging
        for df in [actuals, budget, fx]:
            if 'currency' in df.columns:
                df['currency'] = df['currency'].str.strip()
        
        # convert month columns to datetime objects for proper filtering
        for df in [actuals, budget, cash, fx]:
            df['month'] = pd.to_datetime(df['month'])

        # merge with fx rates to get the conversion rate
        actuals = pd.merge(actuals, fx, on=['month', 'currency'], how='left')
        # Any value already in USD won't find a match, so its rate will be NaN. filk it with 1.0
        actuals['rate_to_usd'] = actuals['rate_to_usd'].fillna(1.0)
        # Create a unified 'value_usd' column for all calculations
        actuals['value_usd'] = actuals['value'] * actuals['rate_to_usd']
        
        # Repeat the same logic for the budget data
        budget = pd.merge(budget, fx, on=['month', 'currency'], how='left')
        budget['rate_to_usd'] = budget['rate_to_usd'].fillna(1.0)
        budget['value_usd'] = budget['value'] * budget['rate_to_usd']

        return {'actuals': actuals, 'budget': budget, 'cash': cash, 'fx': fx}

    def get_opex_breakdown(self, month_str: str):
        try:
            target_date = datetime.strptime(month_str, "%B %Y")
        except ValueError:
            return {"text": f"Error: Invalid date format received: '{month_str}'. Please use 'Month YYYY'.", "chart": None}

        # Filter the pre-processed data for the correct month and Opex accounts
        opex_data = self.data['actuals'][
            (self.data['actuals']['month']  == target_date) &
            (self.data['actuals']['account_c'].str.startswith('Opex:'))
        ].copy()

        # Create a clean 'category' column (e.g., 'Opex:Marketing' -> 'Marketing')
        opex_data['category'] = opex_data['account_c'].str.split(':').str[1].str.strip()
        
        breakdown = opex_data.groupby('category')['value_usd'].sum()
        
        if breakdown.empty:
            return {"text": f"No Opex data found for {month_str}.", "chart": None}

        fig, ax = plt.subplots(figsize=(6, 4.5))
        breakdown.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
        ax.set_title(f'Opex Breakdown - {month_str}')
        ax.set_ylabel('') 
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        total_opex = breakdown.sum()
        summary = f"**Opex Breakdown for {month_str} (Total: `${total_opex:,.0f}` USD):**\n"
        # Sort the categories by value for a more organized report
        for category, value in breakdown.sort_values(ascending=False).items():
            summary += f"- **{category}:** `${value:,.0f}`\n"

        return {"text": summary, "chart": buf}
    
    def get_revenue_vs_budget(self, month_str: str):
        try:
            target_date = datetime.strptime(month_str, "%B %Y")
        except ValueError:
            return {"text": f"Error: Invalid date format received: '{month_str}'. Please use 'Month YYYY'.", "chart": None}

        actual_rev = self.data['actuals'][
            (self.data['actuals']['month'] == target_date) &
            (self.data['actuals']['account_c'] == 'Revenue')
        ]['value_usd'].sum()

        budget_rev = self.data['budget'][
            (self.data['budget']['month'] == target_date) &
            (self.data['budget']['account_c'] == 'Revenue')
        ]['value_usd'].sum()

        variance = actual_rev - budget_rev
        
        fig, ax = plt.subplots(figsize=(6, 4))
        categories = ['Actual', 'Budget']
        values = [actual_rev, budget_rev]
        ax.bar(categories, values, color=['#4CAF50', '#2196F3'])
        ax.set_title(f'Revenue vs. Budget - {month_str}')
        ax.set_ylabel('Amount (USD)')
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        summary = (
            f"**Revenue for {month_str}:**\n"
            f"- **Actual:** `${actual_rev:,.0f}` USD\n"
            f"- **Budget:** `${budget_rev:,.0f}` USD\n"
            f"- **Variance:** `${variance:,.0f}` USD"
        )
        return {"text": summary, "chart": buf}

    def get_gross_margin_trend(self, num_months=3):
        latest_date = self.data['actuals']['month'].max()
        start_date = latest_date - relativedelta(months=num_months - 1)
        
        df = self.data['actuals'][self.data['actuals']['month'] >= start_date].copy()
        
        monthly_data = df.pivot_table(index='month', columns='account_c', values='value_usd', aggfunc='sum')
        monthly_data = monthly_data.fillna(0)

        monthly_data['Gross Margin'] = monthly_data['Revenue'] - monthly_data.get('COGS', 0)
        monthly_data['Gross Margin %'] = (monthly_data['Gross Margin'] / monthly_data['Revenue']) * 100
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(monthly_data.index.strftime('%b %Y'), monthly_data['Gross Margin %'], marker='o', linestyle='-')
        ax.set_title(f'Gross Margin % Trend (Last {num_months} Months)')
        ax.set_ylabel('Gross Margin %')
        ax.set_xlabel('Month')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        summary = f"**Gross Margin % Trend (Last {num_months} Months):**\n"
        for month, row in monthly_data.iterrows():
            summary += f"- **{month.strftime('%B %Y')}:** `{row['Gross Margin %']:.1f}%`\n"
            
        return {"text": summary, "chart": buf}

    def get_cash_runway(self):
        cash_df = self.data['cash'].sort_values('month').copy()
        cash_df['burn'] = -cash_df['cash_balance'].diff()
        
        avg_burn = cash_df['burn'].tail(3).mean()
        current_cash = cash_df['cash_balance'].iloc[-1]
        
        if avg_burn <= 0:
            return {"text": "**Cash Runway:** Not applicable (no average net burn).", "chart": None}
            
        runway_months = current_cash / avg_burn
        
        summary = (
            f"**Cash Runway Analysis:**\n"
            f"- **Current Cash Balance:** `${current_cash:,.0f}`\n"
            f"- **Avg. 3-Month Net Burn:** `${avg_burn:,.0f}` / month\n"
            f"- **Estimated Cash Runway:** `{runway_months:.1f}` months"
        )
        return {"text": summary, "chart": None}

    def get_ebitda_proxy(self, month_str: str):
        try:
            target_date = datetime.strptime(month_str, "%B %Y")
        except ValueError:
            return {"text": f"Error: Invalid date format received: '{month_str}'. Please use 'Month YYYY'.", "chart": None}

        month_data = self.data['actuals'][self.data['actuals']['month'] == target_date]

        revenue = month_data[month_data['account_c'] == 'Revenue']['value_usd'].sum()
        cogs = month_data[month_data['account_c'] == 'COGS']['value_usd'].sum()
        opex = month_data[month_data['account_c'].str.startswith('Opex:')]['value_usd'].sum()

        if revenue == 0:
            return {"text": f"No revenue data found for {month_str} to calculate EBITDA.", "chart": None}

        ebitda = revenue - cogs - opex

        summary = (
            f"**EBITDA (Proxy) for {month_str}:**\n"
            f"- **Revenue:** `${revenue:,.0f}`\n"
            f"- **COGS:** `${cogs:,.0f}`\n"
            f"- **Opex:** `${opex:,.0f}`\n"
            f"--------------------\n"
            f"- **EBITDA:** `${ebitda:,.0f}`"
        )
        return {"text": summary, "chart": None}

