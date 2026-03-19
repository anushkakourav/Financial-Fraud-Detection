import pandas as pd
from src.config import (
    TRAIN_FILE,
    TEST_FILE,
    CLEANED_TRAIN_FILE,
    CLEANED_TEST_FILE,
)

# ======================================================
# FINAL COLUMNS TO KEEP
# ======================================================
SELECTED_COLUMNS = [
    "amt",
    "unix_time",
    "city_pop",
    "merchant",
    "category",
    "zip",
    "lat",
    "long",
    "merch_lat",
    "merch_long",
    "dob",
    "trans_date_trans_time",
    "is_fraud",
]


# ======================================================
# PREPROCESSING FUNCTION
# ======================================================

def preprocess_dataframe(df):
    df = df.copy()

    # -----------------------------
    # KEEP ONLY REQUIRED COLUMNS
    # -----------------------------
    df = df[SELECTED_COLUMNS]

    # -----------------------------
    # DATETIME → FEATURES
    # -----------------------------
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

    df["trans_hour"] = df["trans_date_trans_time"].dt.hour
    df["trans_day"] = df["trans_date_trans_time"].dt.day
    df["trans_month"] = df["trans_date_trans_time"].dt.month

    df.drop(columns=["trans_date_trans_time"], inplace=True)

    # -----------------------------
    # DOB → AGE
    # -----------------------------
    df["dob"] = pd.to_datetime(df["dob"])
    df["age"] = (pd.Timestamp.now() - df["dob"]).dt.days // 365
    df.drop(columns=["dob"], inplace=True)

    # -----------------------------
    # DISTANCE FEATURE
    # -----------------------------
    df["distance"] = (
        (df["lat"] - df["merch_lat"]) ** 2 +
        (df["long"] - df["merch_long"]) ** 2
    ) ** 0.5

    df.drop(columns=["lat", "long", "merch_lat", "merch_long"], inplace=True)

    # -----------------------------
    # HANDLE MISSING VALUES
    # -----------------------------
    df.ffill(inplace=True)

    return df


# ======================================================
# MAIN
# ======================================================

def main():

    print("Loading datasets...")

    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)

    print("Preprocessing train data...")
    train_df = preprocess_dataframe(train_df)

    print("Preprocessing test data...")
    test_df = preprocess_dataframe(test_df)

    print("Saving cleaned files...")

    train_df.to_csv(CLEANED_TRAIN_FILE, index=False)
    test_df.to_csv(CLEANED_TEST_FILE, index=False)

    print("✅ Data preprocessing completed.")


if __name__ == "__main__":
    main()