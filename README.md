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

Step 1: Clone the Repository

Step 2: py -3.11 -m pip install -r requirements.txt

Step 3: Download Dataset:

 https://www.kaggle.com/datasets/kartik2112/fraud-detection
 
Place the dataset files in:  data/raw/

Step 4: py -3.11 -m src.data_preprocessing

Step 5: py -3.11 -m pip install imbalanced-learn

Step 6: py -3.11 -m src.feature_engineering

Step 7: py -3.11 -m src.train_logistic_regression

Step 8: py -3.11 -m src.train_random_forest

Step 9: py -3.11 -m src.train_xgboost

Step 10: py -3.11 -m src.train_lightgbm

Step 11: py -3.11 -m src.model_selector

Step 12: py -3.11 -m streaming.consumer

Step 13: py -3.11 -m streaming.producer

Step 14: py -3.11 -m app.app
