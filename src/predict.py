import joblib
import pandas as pd
from src.config import MODELS_DIR
import uuid
from datetime import datetime

FEATURE_COLUMNS = [
    "amt",
    "unix_time",
    "city_pop",
    "trans_hour",
    "trans_day",
    "trans_month",
    "age",
    "distance",
    "merchant",
    "category",
    "zip"
]

CATEGORICAL_COLS = ["merchant", "category", "zip"]

NUMERICAL_COLS = [
    "amt", "unix_time", "city_pop",
    "trans_hour", "trans_day", "trans_month",
    "age", "distance"
]

THRESHOLD = 0.85


# =====================================================
# Load trained artifacts
# =====================================================

def load_artifacts():
    model = joblib.load(MODELS_DIR / "best_model.pkl")
    scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    freq_mappings = joblib.load(MODELS_DIR / "freq_mappings.pkl")

    return model, scaler, freq_mappings


model, scaler, freq_mappings = load_artifacts()


# =====================================================
# Preprocessing
# =====================================================

def preprocess_input(input_data):

    df = pd.DataFrame([input_data])

    # Frequency Encoding
    for col in CATEGORICAL_COLS:
        df[col] = df[col].map(freq_mappings[col]).fillna(0)

    # Scaling
    df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS])

    return df[FEATURE_COLUMNS]


# =====================================================
# Prediction Function (used by Kafka Consumer)
# =====================================================

def predict_transaction(transaction_dict):

    processed_df = preprocess_input(transaction_dict)

    probability = model.predict_proba(processed_df)[0][1]

    prediction = 1 if probability > THRESHOLD else 0

    return int(prediction), float(probability)

# =====================================================
# CLI Prediction (Manual testing)
# =====================================================

def main():

    print("🔎 Enter RAW Transaction Details\n")

    input_data = {}

    for col in FEATURE_COLUMNS:
        value = float(input(f"{col}: "))
        input_data[col] = value

    prediction, probability = predict_transaction(input_data)

    print("\n==============================")

    if prediction == 1:
        print("⚠ FRAUD DETECTED")
    else:
        print("✅ NOT FRAUD")

    print(f"Fraud Probability: {probability:.4f}")
    print("==============================")


if __name__ == "__main__":
    main()