# Financial-Fraud-Detection

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
