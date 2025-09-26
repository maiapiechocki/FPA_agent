CFO Copilot: An FP&A Agent
This project is a solution for the FP&A Agent Coding Assignment. It is a Streamlit web application that acts as an AI-powered assistant for a CFO. The agent can answer questions about monthly financial performance by analyzing data from local CSV files, consolidating results from multiple business entities, and generating charts to provide concise, board-ready answers.

✨ Features
Natural Language Chat Interface: Ask questions in plain English.

Automated Financial Metric Calculation: Calculates key metrics on the fly.

Consolidated Reporting: Correctly combines data from ParentCo (USD) and EMEA (EUR) for a true consolidated view.

Dynamic Chart Generation: Creates Matplotlib charts to visualize trends and breakdowns.

Simple & Robust Agent Design: Uses a rules-based planner to interpret user intent without relying on external LLM APIs.

📊 Core Metrics Supported
The agent is designed to calculate and report on the following key financial metrics as per the assignment requirements:

Revenue (USD): Actual vs. Budget performance and variance.

Gross Margin %: Calculated as (Revenue – COGS) / Revenue.

Opex Total (USD): Grouped by major categories (Marketing, Sales, R&D, Admin).

EBITDA (Proxy): Calculated as Revenue – COGS – Opex.

Cash Runway: Calculated as Current Cash Balance ÷ Average 3-Month Net Burn.

🛠️ Tech Stack
Language: Python 3

Web Framework: Streamlit

Data Analysis: Pandas

Charting: Matplotlib

Testing: Pytest

📂 Project Structure
The repository is organized to separate the web application, agent logic, and data.

├── fixtures/
│   ├── actuals.csv
│   ├── budget.csv
│   ├── cash.csv
│   └── fx.csv
├── agent/
│   ├── __init__.py
│   ├── agent.py      # Main agent router
│   ├── planner.py    # Intent classification logic
│   └── tools.py      # Data analysis and calculation functions
├── tests/
│   ├── __init__.py
│   └── test_agent.py # Simple test for the agent
├── app.py            # The Streamlit web application
├── .gitignore        # Specifies files for Git to ignore (e.g., venv)
└── requirements.txt  # Project dependencies

🚀 Setup and Installation
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.9 or higher

pip and venv

1. Clone the Repository
git clone [https://github.com/maiapiechocki/FPA_agent.git](https://github.com/maiapiechocki/FPA_agent.git)
cd FPA_agent

2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python -m venv venv

# Activate it:
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. Install Dependencies
Install all required libraries from the requirements.txt file.

pip install -r requirements.txt

▶️ How to Run the Application
1. Run the Tests (Optional but Recommended)
Before launching, you can run the included test to ensure the agent's core logic is working correctly.

pytest

You should see a confirmation that 1 passed.

2. Launch the Streamlit App
Start the web application with the following command:

streamlit run app.py

The application will automatically open in your default web browser.

❓ Example Questions to Ask the Agent
Here are some sample questions the agent is designed to answer:

"What was June 2025 revenue vs budget in USD?"

"Show Gross Margin % trend for the last 3 months."

"Break down Opex by category for June."

"What is our EBITDA for December 2025?"

"What is our cash runway right now?"
