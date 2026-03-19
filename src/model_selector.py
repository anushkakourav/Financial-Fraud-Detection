import pandas as pd
import joblib

from sklearn.metrics import recall_score, precision_score, roc_auc_score

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

def load_test_data():
    test_df = pd.read_csv(FINAL_TEST_FILE)

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    return X_test, y_test


# ======================================================
# EVALUATE MODEL
# ======================================================

def evaluate_model(model, X_test, y_test):

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    return recall, precision, roc_auc


# ======================================================
# MAIN
# ======================================================

def main():

    print("Loading test dataset...")
    X_test, y_test = load_test_data()

    model_files = {
        "logistic_regression": MODELS_DIR / "logistic_regression.pkl",
        "random_forest": MODELS_DIR / "random_forest.pkl",
        "xgboost": MODELS_DIR / "xgboost.pkl",
        "lightgbm": MODELS_DIR / "lightgbm.pkl"
    }

    results = []

    print("\nEvaluating models...\n")

    for name, path in model_files.items():

        model = joblib.load(path)

        recall, precision, roc_auc = evaluate_model(model, X_test, y_test)

        print(f"{name.upper()}")
        print(f"Recall (Fraud): {recall:.4f}")
        print(f"Precision (Fraud): {precision:.4f}")
        print(f"ROC-AUC: {roc_auc:.4f}\n")

        results.append({
            "model": name,
            "recall": recall,
            "precision": precision,
            "roc_auc": roc_auc
        })

    results_df = pd.DataFrame(results)

    # 🔥 PRIORITIZE RECALL
    best_model_row = results_df.sort_values(by="recall", ascending=False).iloc[0]
    best_model_name = best_model_row["model"]

    print("===================================")
    print(f"🏆 Best Model Based on Recall: {best_model_name.upper()}")
    print("===================================")

    # Save best model
    best_model = joblib.load(model_files[best_model_name])
    joblib.dump(best_model, MODELS_DIR / "best_model.pkl")

    # Save comparison report
    comparison_path = REPORTS_DIR / "model_metrics.csv"
    results_df.to_csv(comparison_path, index=False)

    print("\n✅ Best model saved as best_model.pkl")
    print("✅ Model comparison saved as model_metrics.csv")


if __name__ == "__main__":
    main()