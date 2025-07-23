from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.artifact_entity import DataIngestionArtifact
import os 
import sys 
import numpy as np 
import pandas as pd 
import pymongo
from typing import List 
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv() 

MONGO_DB_URL=os.getenv('MONGO_DB_URL') 

class Dataingestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def export_collection_asdf(self):
        '''
        read from mongodb
        '''
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name] 
            
            df=pd.DataFrame(list(collection.find())) 
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1) 
                
            df.replace({"na":np.nan},inplace=True)
            return df
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def export_df_into_featurestore(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path) 
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def splitting_data(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("data splits into train and test set")
            
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info("exporting train and test file path")
            
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True) 
            
            logging.info("exported test and train path")
            
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
         
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_asdf()
            dataframe=self.export_df_into_featurestore(dataframe)
            self.splitting_data(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.test_file_path) 
            
            return dataingestionartifact      
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
         
            
            
              
            