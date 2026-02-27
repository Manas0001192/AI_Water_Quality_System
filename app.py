import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from wqi import calculate_wqi
from risk_engine import classify_risk
from email_alert import send_email_alert

st.set_page_config(layout="wide")
st.title("💧 AI Water Intelligence Monitoring System")

# Load Model
model = joblib.load("model.pkl")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", [
    "Executive Dashboard",
    "Data Center",
    "Advanced Analytics",
    "AI Intelligence",
    "Control Room",
    "Admin Panel"
])

uploaded_file = st.sidebar.file_uploader("Upload Water Quality CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

    # Remove Potability if exists
    if "Potability" in df.columns:
        df_input = df.drop("Potability", axis=1)
    else:
        df_input = df.copy()

    predictions = model.predict(df_input)
    probabilities = model.predict_proba(df_input)[:, 1]

    df["ML_Prediction"] = predictions
    df["ML_Probability"] = probabilities
    df["WQI"] = df.apply(calculate_wqi, axis=1)

    df["Risk_Level"] = df.apply(
        lambda row: classify_risk(row["WQI"], row["ML_Probability"]),
        axis=1
    )

    # ---------------- Executive Dashboard ----------------
    if page == "Executive Dashboard":

        st.header("📊 Water Quality Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Safe Zones", (df["Risk_Level"] == "SAFE").sum())
        col2.metric("Warning Zones", (df["Risk_Level"] == "WARNING").sum())
        col3.metric("Critical Zones", (df["Risk_Level"] == "CRITICAL").sum())

        st.subheader("Risk Distribution")
        st.bar_chart(df["Risk_Level"].value_counts())

        st.subheader("Average Water Quality Index")
        st.metric("Average WQI", round(df["WQI"].mean(), 2))

    # ---------------- Data Center ----------------
    elif page == "Data Center":
        st.header("📂 Raw Data & Processed Results")
        st.write(df.head())
        st.download_button("Download Processed Report",
                           df.to_csv(index=False),
                           "processed_report.csv")

    # ---------------- Advanced Analytics ----------------
    elif page == "Advanced Analytics":

        st.header("📈 Advanced Data Analytics")

        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(df.corr(numeric_only=True),
                    annot=True,
                    cmap="coolwarm",
                    ax=ax)
        st.pyplot(fig)

        st.subheader("Outlier Detection (Boxplot)")
        numeric_cols = df.select_dtypes(include=['float64','int64']).columns
        selected_col = st.selectbox("Select Parameter", numeric_cols)

        fig2, ax2 = plt.subplots()
        sns.boxplot(y=df[selected_col], ax=ax2)
        st.pyplot(fig2)

    # ---------------- AI Intelligence ----------------
    elif page == "AI Intelligence":

        st.header("🤖 AI Model Intelligence")

        st.subheader("Prediction Probability Distribution")
        st.histogram = st.bar_chart(df["ML_Probability"])

        st.subheader("Feature Importance")

        importances = model.named_steps["model"].feature_importances_
        features = df_input.columns

        importance_df = pd.DataFrame({
            "Feature": features,
            "Importance": importances
        }).sort_values("Importance", ascending=False)

        st.bar_chart(importance_df.set_index("Feature"))

    # ---------------- Control Room ----------------
    elif page == "Control Room":

        st.header("🚨 Live Risk Monitoring Control Room")

        critical_df = df[df["Risk_Level"] == "CRITICAL"]

        st.subheader("Critical Areas Detected")
        st.write(critical_df)

        if st.button("Send Email Alert (Manual Trigger)"):
            send_email_alert(df)
            st.success("Email Alert Sent Successfully")

        st.subheader("Smart Recommendations")

        recommendations = []

        if df["WQI"].mean() > 150:
            recommendations.append("⚠ Improve filtration systems immediately.")

        if df["ML_Probability"].mean() < 0.5:
            recommendations.append("⚠ Conduct urgent water quality audit.")

        if not recommendations:
            recommendations.append("✅ Water quality currently under control.")

        for rec in recommendations:
            st.write(rec)

    # ---------------- Admin Panel ----------------
    elif page == "Admin Panel":

        st.header("⚙ System & Model Insights")

        st.subheader("Dataset Summary")
        st.write(df.describe())

        st.subheader("Model Details")
        st.write("Algorithm: Random Forest")
        st.write("Number of Features:", len(df_input.columns))

        st.subheader("Top 5 Risky Samples")
        st.write(df.sort_values("WQI", ascending=False).head())

else:
    st.info("Upload a CSV file from sidebar to begin analysis.")