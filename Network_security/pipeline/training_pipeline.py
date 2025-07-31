import os,sys

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging 

from Network_security.components.data_ingestion import Dataingestion
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DataTransformation
from Network_security.components.model_trainer import ModelTrainer

from Network_security.entity.config_entity import(
    trainingpipelineconfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from Network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DatavalidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

from Network_security.constant.training_pipeline import TRAINING_BUCKET_NAME
from Network_security.constant.training_pipeline import SAVED_MODEL_DIR

##this file is corresponding to main.py
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=trainingpipelineconfig()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            logging.info("data ingestion is initiated")
            data_ingestion=Dataingestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion is completed and artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("data validation is started")
            datavalidation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=datavalidation.initiate_data_validation()
            logging.info("data validation is completed")
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
         
    def start_data_transformation(self,data_validation_artifact:DatavalidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("data transformation is initiated")
            datatransformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact=datatransformation.initiate_data_tranformation()
            logging.info("data transformation is completed")
            return data_transformation_artifact
            
        except Exception as e:
            raise  NetworkSecurityexception(e,sys) 
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("model training is started")
            modeltraining=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.data_transformation_config) 
            model_trainer_artifact=modeltraining.initiate_model_training()
            logging.info("model training is completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
            
            
            