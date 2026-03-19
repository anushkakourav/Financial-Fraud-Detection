# Financial-Fraud-Detection

Dataset
   │
   ▼
Data Preprocessing
   │
   ▼
Feature Engineering
   │
   ▼
Machine Learning Models
(Logistic Regression, Random Forest, XGBoost, LightGBM)
   │
   ▼
Model Selection
   │
   ▼
Best Model Saved
   │
   ▼
Kafka Producer → Kafka Topic → Kafka Consumer
                              │
                              ▼
                        Fraud Prediction
                              │
                              ▼
                         SQLite Database
                              │
                              ▼
                   Flask Web Application
                              │
                              ▼
                       Analytics Dashboard


py -3.11 -m pip install -r requirements.txt

py -3.11 -m src.data_preprocessing

py -3.11 -m pip install imbalanced-learn

py -3.11 -m src.feature_engineering

py -3.11 -m src.train_logistic_regression

py -3.11 -m src.train_random_forest

py -3.11 -m src.train_xgboost

py -3.11 -m src.train_lightgbm

py -3.11 -m src.model_selector

py -3.11 -m streaming.consumer

py -3.11 -m streaming.producer

py -3.11 -m app.app
