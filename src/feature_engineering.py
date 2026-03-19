import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler

from src.config import (
    CLEANED_TRAIN_FILE,
    CLEANED_TEST_FILE,
    FINAL_TRAIN_FILE,
    FINAL_TEST_FILE,
    TARGET_COLUMN,
    MODELS_DIR
)

NUMERICAL_COLS = [
    "amt", "unix_time", "city_pop",
    "trans_hour", "trans_day", "trans_month",
    "age", "distance"
]

CATEGORICAL_COLS = ["merchant", "category", "zip"]


# ======================================================
# FEATURE ENGINEERING
# ======================================================

def feature_engineering(train_df, test_df):

    train_df = train_df.copy()
    test_df = test_df.copy()

    y_train = train_df[TARGET_COLUMN].copy()
    y_test = test_df[TARGET_COLUMN].copy()

    X_train = train_df.drop(columns=[TARGET_COLUMN]).copy()
    X_test = test_df.drop(columns=[TARGET_COLUMN]).copy()

    # 🔹 Frequency Encoding (FIT ON TRAIN ONLY)
    freq_mappings = {}

    for col in CATEGORICAL_COLS:
        freq_dict = X_train[col].value_counts().to_dict()
        freq_mappings[col] = freq_dict

        X_train[col] = X_train[col].map(freq_dict)
        X_test[col] = X_test[col].map(freq_dict)

        X_test[col] = X_test[col].fillna(0)

    # 🔹 Scaling (FIT ON TRAIN ONLY)
    scaler = StandardScaler()
    X_train[NUMERICAL_COLS] = scaler.fit_transform(X_train[NUMERICAL_COLS])
    X_test[NUMERICAL_COLS] = scaler.transform(X_test[NUMERICAL_COLS])

    # 🔹 Final NaN Safety
    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)

    # 🔥 SAVE ARTIFACTS FOR PRODUCTION PREDICTION
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    joblib.dump(freq_mappings, MODELS_DIR / "freq_mappings.pkl")

    return X_train, y_train, X_test, y_test


# ======================================================
# CLASS BALANCING
# ======================================================

def balance_data(X_train, y_train):

    print("\nBefore balancing:")
    print(y_train.value_counts())

    rus = RandomUnderSampler(random_state=42)

    X_res, y_res = rus.fit_resample(X_train, y_train)

    X_res = pd.DataFrame(X_res, columns=X_train.columns).reset_index(drop=True)
    y_res = pd.Series(y_res).reset_index(drop=True)

    print("\nAfter balancing:")
    print(y_res.value_counts())

    return X_res, y_res


# ======================================================
# MAIN
# ======================================================

def main():

    print("Loading cleaned datasets...")
    train_df = pd.read_csv(CLEANED_TRAIN_FILE)
    test_df = pd.read_csv(CLEANED_TEST_FILE)

    print("\nPerforming feature engineering...")
    X_train, y_train, X_test, y_test = feature_engineering(train_df, test_df)

    print("\nHandling class imbalance...")
    X_train, y_train = balance_data(X_train, y_train)

    # 🔥 Reset Index Before Saving
    X_train = X_train.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    final_train = pd.concat([X_train, y_train], axis=1)
    final_test = pd.concat([X_test, y_test], axis=1)

    print("\nNaN check (TRAIN FILE):", final_train.isna().sum().sum())
    print("NaN check (TEST FILE):", final_test.isna().sum().sum())

    final_train.to_csv(FINAL_TRAIN_FILE, index=False)
    final_test.to_csv(FINAL_TEST_FILE, index=False)

    print("✅ Feature engineering completed.")
    print("✅ scaler.pkl saved")
    print("✅ freq_mappings.pkl saved")


if __name__ == "__main__":
    main()