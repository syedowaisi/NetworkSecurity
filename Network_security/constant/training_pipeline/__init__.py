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

# SCHEMA_FILE_PATH:str=""


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="OWAISI"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

