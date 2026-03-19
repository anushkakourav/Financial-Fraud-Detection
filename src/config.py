from pathlib import Path

# ======================================================
# PROJECT ROOT  (D:\Finantial Fraud detection)
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# DATA PATHS
# ======================================================
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

TRAIN_FILE = RAW_DATA_DIR / "fraudTrain.csv"
TEST_FILE = RAW_DATA_DIR / "fraudTest.csv"

CLEANED_TRAIN_FILE = PROCESSED_DATA_DIR / "cleaned_train.csv"
CLEANED_TEST_FILE = PROCESSED_DATA_DIR / "cleaned_test.csv"

FINAL_TRAIN_FILE = PROCESSED_DATA_DIR / "final_train.csv"
FINAL_TEST_FILE = PROCESSED_DATA_DIR / "final_test.csv"

# ======================================================
# MODEL PATHS
# ======================================================
MODELS_DIR = BASE_DIR / "models"

LOGISTIC_MODEL = MODELS_DIR / "logistic_regression.pkl"
DECISION_TREE_MODEL = MODELS_DIR / "decision_tree.pkl"
RANDOM_FOREST_MODEL = MODELS_DIR / "random_forest.pkl"
XGBOOST_MODEL = MODELS_DIR / "xgboost.pkl"
BEST_MODEL = MODELS_DIR / "best_model.pkl"

# ======================================================
# REPORT PATHS
# ======================================================
REPORTS_DIR = BASE_DIR / "reports"
CLASSIFICATION_REPORTS_DIR = REPORTS_DIR / "classification_reports"

MODEL_METRICS_FILE = REPORTS_DIR / "model_metrics.csv"
COMPARISON_REPORT_FILE = REPORTS_DIR / "comparison_report.txt"

# ======================================================
# DATABASE PATH
# ======================================================
DATABASE_PATH = BASE_DIR / "fraud_detection.db"

# ======================================================
# TARGET COLUMN
# ======================================================
TARGET_COLUMN = "is_fraud"

# ======================================================
# CREATE FOLDERS IF NOT EXIST
# ======================================================
for folder in [
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    CLASSIFICATION_REPORTS_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ==============================
# Kafka Configuration
# ==============================

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "fraud-transactions"