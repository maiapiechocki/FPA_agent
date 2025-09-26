# 💰 CFO Copilot: An FP&A Agent
A Streamlit web application that acts as an AI-powered assistant for a CFO. This agent answers questions about monthly financial performance by analyzing local CSV files, consolidating results from multiple business entities, and generating charts to provide concise, board-ready answers.

<img width="908" height="900" alt="image" src="https://github.com/user-attachments/assets/2d1c0037-053e-44ec-9127-2717d5a33b92" />

# Core Features
Natural Language Chat Interface: Ask complex financial questions in plain English.

Automated Financial Metric Calculation: Instantly calculates key metrics without manual work.

Consolidated Global Reporting: Correctly combines data from ParentCo (USD) and EMEA (EUR) for a true consolidated view of the business.

Dynamic Chart Generation: Creates clean, professional Matplotlib charts to visualize trends and breakdowns.

Simple & Robust Agent Design: Uses a rules-based planner to interpret user intent reliably and efficiently, without the need for external LLM APIs.

# 📊 Metrics Supported
The agent is designed to calculate and report on the following key financial metrics as per the assignment requirements:

Revenue (USD): Actual vs. Budget performance and variance.

Gross Margin %: Calculated as (Revenue – COGS) / Revenue.

Opex Total (USD): Grouped by major categories (Marketing, Sales, R&D, Admin).

EBITDA (Proxy): Calculated as Revenue – COGS – Opex.

Cash Runway: Calculated as Current Cash Balance ÷ Average 3-Month Net Burn.


# 🚀 Getting Started
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.9 or higher

pip and venv installed

1. Clone the Repository
Bash

git clone https://github.com/maiapiechocki/FPA_agent.git
cd FPA_agent
2. Create and Activate a Virtual Environment
Using a virtual environment is highly recommended to manage project dependencies.

Bash

# Create the virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
Install all required libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
▶️ How to Run
1. Run the Tests (Optional but Recommended)
Before launching, you can run the included test to ensure the agent's core logic is working correctly. From the root directory, run:

Bash

pytest
You should see a confirmation that 1 passed.

2. Launch the Streamlit App
Start the web application with the following command:

Bash

streamlit run app.py
The application will automatically open in your default web browser.

# ❓ Example Questions
Here are some sample questions the agent is designed to answer:

What was June 2025 revenue vs budget in USD?

Show Gross Margin % trend for the last 3 months.

Break down Opex by category for June.

What is our EBITDA for December 2025?

What is our cash runway right now?
