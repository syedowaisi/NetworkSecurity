from Network_security.entity.artifact_entity import DataIngestionArtifact,DatavalidationArtifact
from Network_security.entity.config_entity import DataValidationConfig 
import  os,sys
import pandas as pd

from scipy.stats import ks_2samp
from Network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file
from Network_security.constant.training_pipeline import SCHEMA_FILE_PATH

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging 

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact, 
                 data_validation_config:DataValidationConfig): 
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
                
    def validate_noof_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_columns=len(self.schema_config)
            
            logging.info(f"Required NO. of columns:{number_columns}")
            logging.info(f"DataFrame has columns:{len(dataframe.columns)}")
            
            if len(dataframe.columns)==number_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5)->bool:
        try:
            status=True
            report={}
            
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                    
                report.update({column:{
                    "pvalue":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
                
            drift_report_filepath=self.data_validation_config.driftreport_filepath
            #create directory
            dir_path=os.path.dirname(drift_report_filepath)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_filepath,content=report)
            return status
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
    def initiate_data_validation(self)->DatavalidationArtifact:
        try:
            train_filepath=self.data_ingestion_artifact.trained_file_path
            test_filepath=self.data_ingestion_artifact.test_file_path
            
            #reading the data
            train_df=DataValidation.read_data(train_filepath) 
            test_df=DataValidation.read_data(test_filepath)
            
            status=self.validate_noof_columns(dataframe=train_df)
            if not status:
                error_message="train dataframe doesn't contains all columns"
                
            status=self.validate_noof_columns(dataframe=test_df)
            if not status:
                error_message="test dataframe doesn't conatains all columns"
            
            ##now checking datadrift
            status=self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            
            data_validation_artifact=DatavalidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.driftreport_filepath,
            )            
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys)   
        