import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="AI Finance Advisor", layout="centered")
st.title("💰 AI Finance Advisor")

# Load raw data and train model live
df = pd.read_csv("transactions.csv", parse_dates=["date"])
daily = df.groupby("date")["amount"].sum().reset_index()
daily.columns = ["ds", "y"]
daily = daily.set_index("ds")
daily.index = pd.DatetimeIndex(daily.index).to_period("D")

ts_model = ExponentialSmoothing(daily["y"], trend="add", seasonal="add", seasonal_periods=7).fit()

st.header("📈 Expense Forecast (Next 30 Days)")
forecast = ts_model.forecast(30)
forecast_df = pd.DataFrame({"Predicted Spend": forecast})
forecast_df.index = forecast_df.index.to_timestamp()
st.line_chart(forecast_df)

st.header("💡 Personalized Suggestions")
cluster_profiles = pd.read_csv("cluster_profiles.csv", index_col=0)
overall_avg = cluster_profiles.mean()
for cluster_id in cluster_profiles.index:
    profile = cluster_profiles.loc[cluster_id]
    flagged = [cat for cat in profile.index if profile[cat] > overall_avg[cat] * 1.15]
    st.subheader(f"Spending Pattern {cluster_id}")
    if flagged:
        for cat in flagged:
            st.write(f"- Your **{cat}** spending tends to run high — consider setting a monthly cap.")
    else:
        st.write("- Spending looks balanced across categories.")
