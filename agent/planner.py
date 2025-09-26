import re
from datetime import datetime

def plan_intent(query: str):
    
    query = query.lower()
    
    # pattern to find a month and an optional year
    date_pattern = r'\b(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+(\d{4}))?\b'
    match = re.search(date_pattern, query)
    
    month_str = "December 2025" # default if no month is found at all
    
    if match:
        month = match.group(1).capitalize()
        year = match.group(2)
        
        if year:
            month_str = f"{month} {year}"
        else:
            month_str = f"{month} 2025"

    intent = "unknown"
    if "revenue" in query and "budget" in query:
        intent = "get_revenue_vs_budget"
    elif "gross margin" in query:
        intent = "get_gross_margin_trend"
    elif "opex" in query or "operating expenses" in query:
        intent = "get_opex_breakdown"
    elif "cash runway" in query:
        intent = "get_cash_runway"
    elif "ebitda" in query:
        intent = "get_ebitda_proxy"
    
    return {"intent": intent, "month": month_str}