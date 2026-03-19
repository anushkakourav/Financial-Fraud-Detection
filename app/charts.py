import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.config import DATABASE_PATH


# -------------------------------------------------
# Load Data From SQLite
# -------------------------------------------------

def load_data():

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM transactions",
        conn
    )

    conn.close()

    return df


# -------------------------------------------------
# 1 Risk Level Distribution
# -------------------------------------------------

def risk_distribution_chart():

    df = load_data()

    counts = df["risk_level"].value_counts().reset_index()
    counts.columns = ["risk_level", "count"]

    fig = px.bar(
        counts,
        x="risk_level",
        y="count",
        color="risk_level",
        title="Risk Level Distribution"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 2 Fraud Probability Histogram
# -------------------------------------------------

def probability_distribution_chart():

    df = load_data()

    fig = px.histogram(
        df,
        x="probability",
        nbins=30,
        title="Fraud Probability Distribution"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 3 Transaction Amount Distribution
# -------------------------------------------------

def amount_distribution_chart():

    df = load_data()

    fig = px.histogram(
        df,
        x="amt",
        nbins=40,
        title="Transaction Amount Distribution"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 4 Transactions by Category
# -------------------------------------------------

def category_chart():

    df = load_data()

    cat = df.groupby("category").size().reset_index(name="count")

    fig = px.bar(
        cat,
        x="category",
        y="count",
        title="Transactions by Category"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 5 Probability vs Amount
# -------------------------------------------------

def probability_vs_amount_chart():

    df = load_data()

    fig = px.scatter(
        df,
        x="amt",
        y="probability",
        color="risk_level",
        title="Probability vs Amount"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 6 Probability Boxplot
# -------------------------------------------------

def probability_boxplot():

    df = load_data()

    fig = px.box(
        df,
        y="probability",
        color="risk_level",
        title="Fraud Probability Spread"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 7 Transaction Count by Risk Level
# -------------------------------------------------

def risk_pie_chart():

    df = load_data()

    counts = df["risk_level"].value_counts()

    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title="Risk Level Percentage"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 8 Amount vs Risk Level
# -------------------------------------------------

def amount_vs_risk_chart():

    df = load_data()

    fig = px.box(
        df,
        x="risk_level",
        y="amt",
        title="Amount Distribution by Risk Level"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 9 Category vs Risk Heatmap
# -------------------------------------------------

def category_risk_heatmap():

    df = load_data()

    table = pd.crosstab(df["category"], df["risk_level"])

    fig = px.imshow(
        table,
        title="Category vs Risk Level Heatmap"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 10 Transaction Trend Over Time
# -------------------------------------------------

def transaction_trend_chart():

    df = load_data()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    trend = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")

    fig = px.line(
        trend,
        x="timestamp",
        y="count",
        title="Transaction Trend Over Time"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 11 Fraud Trend
# -------------------------------------------------

def fraud_trend_chart():

    df = load_data()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fraud = df[df["risk_level"] == "CRITICAL FRAUD"]

    trend = fraud.groupby(fraud["timestamp"].dt.date).size().reset_index(name="count")

    fig = px.line(
        trend,
        x="timestamp",
        y="count",
        title="Critical Fraud Trend"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 12 Probability Density
# -------------------------------------------------

def probability_density_chart():

    df = load_data()

    fig = px.density_contour(
        df,
        x="amt",
        y="probability",
        title="Fraud Density"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 13 Risk vs Amount Scatter
# -------------------------------------------------

def risk_amount_scatter():

    df = load_data()

    fig = px.scatter(
        df,
        x="amt",
        y="probability",
        color="risk_level",
        title="Risk vs Amount Scatter"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 14 Category Distribution Pie
# -------------------------------------------------

def category_pie_chart():

    df = load_data()

    counts = df["category"].value_counts()

    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title="Category Distribution"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 15 Probability vs Category
# -------------------------------------------------

def probability_category_chart():

    df = load_data()

    fig = px.box(
        df,
        x="category",
        y="probability",
        title="Probability by Category"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 16 Risk vs Transaction Count
# -------------------------------------------------

def risk_count_chart():

    df = load_data()

    counts = df["risk_level"].value_counts().reset_index()
    counts.columns = ["risk_level", "count"]

    fig = px.bar(
        counts,
        x="risk_level",
        y="count",
        title="Transaction Count by Risk"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 17 Amount KDE
# -------------------------------------------------

def amount_density_chart():

    df = load_data()

    fig = px.density_contour(
        df,
        x="amt",
        title="Amount Density"
    )

    return fig.to_html(full_html=False)


# -------------------------------------------------
# 18 Probability Trend
# -------------------------------------------------

def probability_trend_chart():

    df = load_data()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    trend = df.groupby(df["timestamp"].dt.date)["probability"].mean().reset_index()

    fig = px.line(
        trend,
        x="timestamp",
        y="probability",
        title="Average Fraud Probability Trend"
    )

    return fig.to_html(full_html=False)