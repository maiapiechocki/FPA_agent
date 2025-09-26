import streamlit as st
import pandas as pd
from agent.agent import FinancialAgent

def load_all_data():
   
    data = {
        'actuals': pd.read_csv('fixtures/actuals.csv', dtype={'amount': float}),
        'budget': pd.read_csv('fixtures/budget.csv', dtype={'amount': float}),
        'cash': pd.read_csv('fixtures/cash.csv'),
        'fx': pd.read_csv('fixtures/fx.csv', dtype={'rate_to_usd': float})
    }
    return data

st.set_page_config(
    page_title="CFO Copilot",
    page_icon="💰",
    layout="centered"
)

st.title("🤖 CFO Copilot")

# init agent in session state
if "agent" not in st.session_state:
    financial_data = load_all_data()
    st.session_state.agent = FinancialAgent(financial_data)

# init chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you analyze your financials today?"}]

# display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "chart" in message and message["chart"] is not None:
            st.image(message["chart"], width=400)

# accept user input
if prompt := st.chat_input("What was June 2025 revenue vs budget?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # fresh agent instance to ensure statelessness
            financial_data = load_all_data()
            agent = FinancialAgent(financial_data)
            response = agent.run(prompt)
            
            response_text = response.get("text")
            response_chart = response.get("chart")

            st.markdown(response_text)
            if response_chart:
                st.image(response_chart, width=400)
            
            assistant_message = {"role": "assistant", "content": response_text}
            if response_chart:
                assistant_message["chart"] = response_chart
            st.session_state.messages.append(assistant_message)

