import pandas as pd
from agent.agent import FinancialAgent

def test_agent_handles_unknown_intent():
    """
    Tests that the agent returns a graceful fallback message
    when it doesn't understand the user's query.
    """
    # Create dummy dataframes for initialization.
    # CRITICAL FIX: We explicitly define the data types (dtype) for each column.
    # This ensures that the 'currency' column is created as a string ('object') type,
    # which prevents the ".str accessor" error during data preparation.
    data = {
        'actuals': pd.DataFrame({
            'month': pd.Series(dtype='datetime64[ns]'),
            'account_category': pd.Series(dtype='object'),
            'amount': pd.Series(dtype='float64'),
            'currency': pd.Series(dtype='object')
        }),
        'budget': pd.DataFrame({
            'month': pd.Series(dtype='datetime64[ns]'),
            'account_category': pd.Series(dtype='object'),
            'amount': pd.Series(dtype='float64'),
            'currency': pd.Series(dtype='object')
        }),
        'cash': pd.DataFrame({
            'month': pd.Series(dtype='datetime64[ns]'),
            'entity': pd.Series(dtype='object'),
            'cash_usd': pd.Series(dtype='float64')
        }),
        'fx': pd.DataFrame({
            'month': pd.Series(dtype='datetime64[ns]'),
            'currency': pd.Series(dtype='object'),
            'rate_to_usd': pd.Series(dtype='float64')
        })
    }
    
    agent = FinancialAgent(data)
    
    # This query does not match any known intent in the planner
    query = "What is the weather like?"
    result = agent.run(query)
    
    # Assert that the agent provides the expected fallback response
    assert "I can answer questions about" in result['text']
    assert result['chart'] is None

