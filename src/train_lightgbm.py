import pandas as pd
import joblib

from lightgbm import LGBMClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from src.config import (
    FINAL_TRAIN_FILE,
    FINAL_TEST_FILE,
    TARGET_COLUMN,
    MODELS_DIR,
    REPORTS_DIR
)


# ======================================================
# LOAD DATA
# ======================================================

def load_data():
    train_df = pd.read_csv(FINAL_TRAIN_FILE)
    test_df = pd.read_csv(FINAL_TEST_FILE)

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    return X_train, y_train, X_test, y_test


# ======================================================
# TRAIN MODEL
# ======================================================

def train_model(X_train, y_train):

    model = LGBMClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=-1,
        num_leaves=31,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    return model


# ======================================================
# EVALUATE MODEL
# ======================================================

def evaluate_model(model, X_test, y_test):

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nROC-AUC Score:")
    print(roc_auc_score(y_test, y_prob))

    report = classification_report(y_test, y_pred)

    print("\nClassification Report:")
    print(report)

    return report


# ======================================================
# SAVE REPORT
# ======================================================

def save_report(report):

    report_path = REPORTS_DIR / "classification_reports" / "lightgbm.txt"

    with open(report_path, "w") as f:
        f.write(report)


# ======================================================
# MAIN
# ======================================================

def main():

    print("Loading final datasets...")

    X_train, y_train, X_test, y_test = load_data()

    print("Training LightGBM model...")

    model = train_model(X_train, y_train)

    print("Evaluating model...")

    report = evaluate_model(model, X_test, y_test)

    print("Saving model...")

    model_path = MODELS_DIR / "lightgbm.pkl"
    joblib.dump(model, model_path)

    print("Saving classification report...")

    save_report(report)

    print("✅ LightGBM training completed.")


if __name__ == "__main__":
    main()