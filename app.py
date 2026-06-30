import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="AI Finance Advisor", layout="centered")
st.title("💰 AI Finance Advisor")

# ---------- SECTION 1: Income & Expenses ----------
st.header("💵 Your Income & Expenses")

input_method = st.radio("How would you like to provide your data?", ["Manual entry", "Upload CSV"])

salary = st.number_input("Monthly Salary (₹)", min_value=0, value=50000, step=1000)

total_expenses = 0
df = None

# Typical spending as % of salary, learned from our dataset's category averages
typical_pct = {
    "Rent": 0.30, "Groceries": 0.10, "Dining": 0.05, "Transport": 0.04,
    "Utilities": 0.04, "Entertainment": 0.03, "Shopping": 0.06, "Healthcare": 0.03
}

if input_method == "Manual entry":
    st.write("**Rent** — enter your exact amount. For other categories, type your own number, or check 'Let AI estimate' to auto-fill a typical value based on your salary.")

    categories = ["Rent", "Groceries", "Dining", "Transport", "Utilities", "Entertainment", "Shopping", "Healthcare"]
    expense_inputs = {}

    # Rent is always manual
    expense_inputs["Rent"] = st.number_input("Rent", min_value=0, value=0, step=500, key="Rent")

    st.write("**Variable expenses:**")
    cols = st.columns(2)
    for i, cat in enumerate(categories[1:]):
        with cols[i % 2]:
            ai_estimate = st.checkbox(f"Let AI estimate {cat}", key=f"ai_{cat}")
            if ai_estimate:
                estimated_value = round(salary * typical_pct[cat])
                st.write(f"AI estimate: ₹{estimated_value:,}")
                expense_inputs[cat] = estimated_value
            else:
                expense_inputs[cat] = st.number_input(cat, min_value=0, value=0, step=500, key=cat)

    total_expenses = sum(expense_inputs.values())

else:
    uploaded_file = st.file_uploader("Upload your transactions CSV (columns: date, category, amount)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, parse_dates=["date"])
        monthly_avg = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().mean()
        total_expenses = round(monthly_avg, 2)
        st.write(f"Average monthly expenses from your data: ₹{total_expenses:,.2f}")
    else:
        st.info("Upload a CSV to continue, or switch to Manual entry.")

surplus = salary - total_expenses

if total_expenses > 0:
    st.metric("Monthly Salary", f"₹{salary:,.0f}")
    st.metric("Monthly Expenses", f"₹{total_expenses:,.0f}")
    st.metric("Monthly Surplus (Investable)", f"₹{surplus:,.0f}")
    
# ---------- SECTION 2: Forecast (uses uploaded CSV if available) ----------
if df is not None:
    st.header("📈 Expense Forecast (Next 30 Days)")
    daily = df.groupby("date")["amount"].sum().reset_index()
    daily.columns = ["ds", "y"]
    daily = daily.set_index("ds")
    daily.index = pd.DatetimeIndex(daily.index).to_period("D")

    if len(daily) >= 14:
        ts_model = ExponentialSmoothing(daily["y"], trend="add", seasonal="add", seasonal_periods=7).fit()
        forecast = ts_model.forecast(30)
        forecast_df = pd.DataFrame({"Predicted Spend": forecast})
        forecast_df.index = forecast_df.index.to_timestamp()
        st.line_chart(forecast_df)
    else:
        st.info("Upload more transaction history (at least 2 weeks) to see a forecast.")

# ---------- SECTION 3: Investment Suggestions ----------
st.header("📊 Investment Allocation Suggestion")
st.caption("Educational suggestions only — not professional financial advice.")

if surplus > 0:
    risk_profile = st.selectbox("Select your risk profile", ["Conservative", "Moderate", "Aggressive"])

    allocations = {
        "Conservative": {"Debt/Liquid Funds": 50, "Mutual Funds (Large Cap)": 30, "Stocks": 10, "Emergency Savings": 10},
        "Moderate": {"Debt/Liquid Funds": 30, "Mutual Funds (Diversified)": 40, "Stocks": 20, "Emergency Savings": 10},
        "Aggressive": {"Debt/Liquid Funds": 10, "Mutual Funds (Equity/SIP)": 30, "Stocks": 50, "Emergency Savings": 10},
    }

    alloc = allocations[risk_profile]
    st.write(f"Based on a **{risk_profile}** risk profile and a monthly surplus of **₹{surplus:,.0f}**, here's a suggested allocation:")

    alloc_df = pd.DataFrame({
        "Category": list(alloc.keys()),
        "Allocation %": list(alloc.values()),
        "Amount (₹)": [round(surplus * pct / 100, 2) for pct in alloc.values()]
    })
    st.dataframe(alloc_df, hide_index=True)
    st.bar_chart(alloc_df.set_index("Category")["Allocation %"])

elif total_expenses > 0:
    st.warning("Your expenses exceed your salary — no surplus available to invest. Consider reviewing your spending first.")

# ---------- SECTION 4: Spending Health Check ----------
if total_expenses > 0:
    st.header("💡 Spending Health Check")
    st.caption("Comparing your spending to typical healthy percentages of income.")

    if input_method == "Manual entry":
        user_expenses = expense_inputs
    else:
        # Break down uploaded CSV into per-category monthly averages
        cat_monthly = df.groupby([df["date"].dt.to_period("M"), "category"])["amount"].sum().reset_index()
        user_expenses = cat_monthly.groupby("category")["amount"].mean().round(2).to_dict()

    flagged_any = False
    for cat, amount in user_expenses.items():
        if cat not in typical_pct or salary == 0:
            continue
        pct_of_salary = amount / salary
        typical = typical_pct[cat]
        if pct_of_salary > typical * 1.2:
            flagged_any = True
            st.write(f"- Your **{cat}** spending is **{pct_of_salary*100:.1f}%** of your salary, "
                      f"higher than the typical **{typical*100:.0f}%** — consider setting a monthly cap.")

    if not flagged_any:
        st.write("Your spending looks balanced relative to typical healthy percentages.")
