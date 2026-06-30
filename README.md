# 💰 AI Finance Advisor

An AI-assisted web app that helps users plan their personal finances — combining expense forecasting, AI-estimated spending, investment allocation suggestions, and a personalized spending health check.

🔗 **Live app:** https://aifinanceadvisor-blhtjb69np6a3hqunfn8ox.streamlit.app/

## Features

- **Income & Expense Tracking** — enter salary and expenses manually, or upload a transaction history CSV.
- **AI-Estimated Spending** — for variable categories (groceries, dining, etc.), users can let the app auto-estimate typical spending as a percentage of income, learned from spending pattern benchmarks.
- **Expense Forecasting** — when transaction history is uploaded, future spending is forecasted using Exponential Smoothing (Holt-Winters), capturing trend and weekly seasonality.
- **Investment Allocation Suggestions** — based on the user's monthly surplus and a selected risk profile (Conservative / Moderate / Aggressive), the app suggests a rule-based percentage allocation across asset categories (mutual funds, stocks, debt/liquid funds, savings). *This is an educational allocation guide, not financial advice.*
- **Spending Health Check** — flags categories where the user's spending significantly exceeds typical healthy percentages of income, with specific numbers and percentages.

## Tech Stack

- **Frontend/App:** Streamlit
- **Forecasting:** statsmodels (Holt-Winters Exponential Smoothing)
- **Data handling:** pandas, numpy
- **Deployment:** Streamlit Community Cloud, GitHub

## How It Works

1. User enters salary and either inputs expenses manually or uploads a CSV of past transactions.
2. Variable expense categories can be auto-filled using AI-estimated typical spending percentages.
3. If transaction history is provided, a time-series model forecasts spending for the next 30 days.
4. Based on monthly surplus and selected risk tolerance, a rule-based engine suggests an investment allocation split.
5. The app compares the user's actual spending percentages against healthy benchmarks and flags categories worth reviewing.

## Running Locally

```bash
git clone https://github.com/kundarrisha/AI_Finance_Advisor.git
cd AI_Finance_Advisor
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

This app is a personal/educational project. Investment suggestions are general allocation guidance based on simple rules, not personalized financial advice. Consult a certified financial advisor for actual investment decisions.

## Author

Built by [kundarrisha](https://github.com/kundarrisha)
