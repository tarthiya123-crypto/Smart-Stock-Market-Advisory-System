from pathlib import Path
import subprocess

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from fetch_data import generate_csv


BASE_DIR = Path(__file__).parent
ANALYZER_PATH = BASE_DIR / "analyzer.exe"
RESULTS_PATH = BASE_DIR / "results.csv"

HORIZON_CODES = {
    "Short Term": "SHORT",
    "Medium Term": "MEDIUM",
    "Long Term": "LONG",
}


def recommendation_reason(recommendation):
    if recommendation == "STRONG BUY":
        return (
            "This stock achieved one of the highest scores in the analysis. "
            "Its growth potential and risk profile align strongly with your preferences."
        )
    if recommendation == "BUY":
        return (
            "This stock shows positive growth momentum and a favorable balance "
            "between risk and expected return."
        )
    if recommendation == "HOLD":
        return (
            "The stock shows moderate potential. It may be suitable for maintaining "
            "exposure, but it is not the strongest current opportunity."
        )
    if recommendation == "WATCH":
        return (
            "The stock has some promising indicators, but current conditions suggest "
            "monitoring it before making a major investment."
        )
    return (
        "The stock currently ranks below stronger alternatives and does not match "
        "the desired risk-return profile as well."
    )


st.set_page_config(page_title="Smart Stock Market Advisory System", layout="wide")

st.title("📈Smart Stock Market Advisory System")
st.markdown("Get stock recommendations based on your investment amount and risk appetite.")

amount = st.number_input("Investment Amount (Rs.)", min_value=1000, value=100000, step=1000)
risk = st.slider("Risk Appetite (%)", min_value=0, max_value=100, value=50)
horizon = st.selectbox("Investment Horizon", ["Short Term", "Medium Term", "Long Term"])

if st.button("Analyze Portfolio"):
    try:
        with st.spinner("Fetching market data..."):
            generate_csv(risk, amount, HORIZON_CODES[horizon])

            if not ANALYZER_PATH.exists():
                st.error("analyzer.exe was not found. Compile the C engine first.")
                st.stop()

            subprocess.run([str(ANALYZER_PATH)], check=True, cwd=BASE_DIR)

        if not RESULTS_PATH.exists():
            st.error("results.csv was not created by analyzer.exe.")
            st.stop()

        results = pd.read_csv(RESULTS_PATH)

        if results.empty:
            st.error("No recommendations were generated.")
            st.stop()

        st.success("Analysis complete.")

        top_stock = results.iloc[0]
        st.markdown("## Top Investment Opportunity")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Stock", top_stock["Stock"])
        with col2:
            st.metric("Score", f"{top_stock['Score']:.2f}")
        with col3:
            st.metric("Recommendation", top_stock["Recommendation"])

        st.success(f"Suggested Investment: Rs. {top_stock['RecommendedInvestment']:,.0f}")

        st.subheader("Price vs Time Comparison")
        top_stocks = results.head(5)["Stock"].tolist()
        price_fig = go.Figure()

        for stock in top_stocks:
            data = yf.download(stock, period="6mo", progress=False, auto_adjust=True)

            if data.empty or "Close" not in data:
                st.warning(f"No price data found for {stock}.")
                continue

            close_prices = data["Close"].dropna().squeeze()

            if close_prices.empty:
                st.warning(f"No closing prices found for {stock}.")
                continue

            normalized = (close_prices / close_prices.iloc[0]) * 100
            price_fig.add_trace(
                go.Scatter(
                    x=normalized.index,
                    y=normalized,
                    mode="lines",
                    name=stock,
                )
            )

        price_fig.update_layout(
            title="Top 5 Stocks Performance Comparison",
            xaxis_title="Date",
            yaxis_title="Indexed Performance (100 = Start)",
            height=500,
        )
        st.plotly_chart(price_fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Investment Amount", f"Rs. {amount:,.0f}")
        with col2:
            st.metric("Risk Appetite", f"{risk}%")
        with col3:
            st.metric("Horizon", horizon)

        st.divider()

        st.subheader("Recommended Stocks")
        st.dataframe(results, use_container_width=True)

        st.subheader("Stock Ranking")
        score_fig = px.bar(
            results,
            x="Stock",
            y="Score",
            text="Score",
            title="Ranking Score Comparison",
        )
        st.plotly_chart(score_fig, use_container_width=True)
        st.subheader("Risk Analysis")
        if risk <= 30:
            st.info("Conservative Investor")
        elif risk <= 70:
            st.warning("Moderate Investor")
        else:
            st.error("Aggressive Investor")

        st.subheader("Insights of top 5 recommended stocks:")
        for rank, (_, row) in enumerate(results.head(5).iterrows(), start=1):
            recommendation = row["Recommendation"]
            reason = recommendation_reason(recommendation)

            st.markdown(
                f"""
                ### #{rank} {row['Stock']}

                **Recommendation:** {recommendation}

                **Analysis Score:** {row['Score']:.2f}/100

                **Suggested Investment:** Rs. {row['RecommendedInvestment']:,.0f}

                **Reason for Selection:** {reason}
                """
            )

    except subprocess.CalledProcessError as error:
        st.error(f"Analyzer failed with exit code {error.returncode}.")
    except Exception as error:
        st.error(f"Something went wrong: {error}")
