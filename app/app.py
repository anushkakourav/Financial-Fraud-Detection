from flask import Flask, render_template, redirect, url_for, session, request
from app.database import get_total_transactions, get_risk_distribution, get_recent_transactions
from app.auth import auth, create_user_table
from src.predict import predict_transaction

# Import ALL charts from charts.py
from app.charts import *

app = Flask(__name__)
app.secret_key = "fraud_detection_secret"

# Register authentication blueprint
app.register_blueprint(auth)

# Create user table on startup
create_user_table()


# -----------------------------
# HOME REDIRECT
# -----------------------------
@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    return redirect(url_for("dashboard"))


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    total_transactions = get_total_transactions()
    risk_distribution = get_risk_distribution()
    recent_transactions = get_recent_transactions()

    # Generate Charts
    chart1 = risk_distribution_chart()
    chart2 = probability_distribution_chart()
    chart3 = amount_distribution_chart()
    chart4 = category_chart()
    chart5 = probability_vs_amount_chart()
    chart6 = probability_boxplot()
    chart7 = risk_pie_chart()
    chart8 = amount_vs_risk_chart()
    chart9 = category_risk_heatmap()
    chart10 = transaction_trend_chart()
    chart11 = fraud_trend_chart()
    chart12 = probability_density_chart()
    chart13 = risk_amount_scatter()
    chart14 = category_pie_chart()
    chart15 = probability_category_chart()
    chart16 = risk_count_chart()
    chart17 = amount_density_chart()
    chart18 = probability_trend_chart()

    return render_template(
        "dashboard.html",
        total=total_transactions,
        risks=risk_distribution,
        transactions=recent_transactions,

        chart1=chart1,
        chart2=chart2,
        chart3=chart3,
        chart4=chart4,
        chart5=chart5,
        chart6=chart6,
        chart7=chart7,
        chart8=chart8,
        chart9=chart9,
        chart10=chart10,
        chart11=chart11,
        chart12=chart12,
        chart13=chart13,
        chart14=chart14,
        chart15=chart15,
        chart16=chart16,
        chart17=chart17,
        chart18=chart18
    )


# -----------------------------
# MANUAL PREDICTION PAGE
# -----------------------------
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        transaction = {
            "amt": float(request.form["amt"]),
            "unix_time": float(request.form["unix_time"]),
            "city_pop": float(request.form["city_pop"]),
            "trans_hour": int(request.form["trans_hour"]),
            "trans_day": int(request.form["trans_day"]),
            "trans_month": int(request.form["trans_month"]),
            "age": int(request.form["age"]),
            "distance": float(request.form["distance"]),
            "merchant": int(request.form["merchant"]),
            "category": int(request.form["category"]),
            "zip": int(request.form["zip"])
        }

        prediction, probability = predict_transaction(transaction)

        # Risk level classification
        if probability < 0.50:
            risk = "LOW RISK"
        elif probability < 0.75:
            risk = "MEDIUM RISK"
        elif probability < 0.90:
            risk = "HIGH RISK"
        else:
            risk = "CRITICAL FRAUD"

        # Redirect to result page
        return render_template(
            "result.html",
            prediction=prediction,
            probability=round(probability, 4),
            risk=risk
        )

    return render_template("predict.html")


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)