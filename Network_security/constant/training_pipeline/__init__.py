import os
import sys 
import pandas as pd
import numpy as np

'''
defining variable for training pipeline
'''
TARGET_NAME="Result"
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACT_DIR: str="Artifacts"
FILE_NAME: str="phisingData.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME: str="test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR=os.path.join("saved_models")
MODEL_FILE_NAME="model.pkl"  


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="OWAISI"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

'''
Data validation related constant
'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl" 

'''
Data transformation related constant
'''
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"
##knn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMETERS:dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",    
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH:str="train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH:str="test.npy"

'''
Model Trainer related Constant
'''
MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float=0.05

TRAINING_BUCKET_NAME:str="networksecurity"  




