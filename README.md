# CFO Copilot - FP&A Agent

This project is a Streamlit web application that acts as an AI-powered assistant for a CFO. It can answer questions about monthly financial performance by analyzing data from local CSV files.

## Features

- **Natural Language Queries**: Ask questions like "What was June 2025 revenue vs budget?" or "Show me gross margin trends".
- **Metric Calculations**: Automatically calculates key financial metrics:
  - Revenue vs. Budget
  - Gross Margin %
  - Opex Breakdown by Category
  - EBITDA (Proxy)
  - Cash Runway
- **Data Visualization**: Generates charts with Matplotlib to visualize trends and breakdowns.
- **Simple Agent Design**: Uses a keyword-based planner to determine user intent and execute the correct data analysis function.

## Project Structure

├── fixtures/
│   ├── actuals.csv
│   ├── budget.csv
│   ├── cash.csv
│   └── fx.csv
├── agent/
│   ├── agent.py      # Main agent router
│   ├── planner.py    # Intent classification logic
│   └── tools.py      # Data analysis and calculation functions
├── tests/
│   └── test_agent.py # Simple test for the agent
├── app.py            # The Streamlit web application
├── requirements.txt  # Project dependencies
└── README.md

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd cfo-copilot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On macOS/Linux
    source venv/bin/activate
    # On Windows
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Run the tests (optional but recommended):**
    ```bash
    pytest
    ```

2.  **Launch the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

The application will open in your web browser.