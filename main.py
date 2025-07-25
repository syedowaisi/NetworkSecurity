from Network_security.components.data_ingestion import Dataingestion
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.config_entity import trainingpipelineconfig

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.entity.config_entity import DataValidationConfig,DataTransformationConfig
from Network_security.components.data_validation import DataValidation 
from Network_security.components.data_transformation import DataTransformation 

from Network_security.components.model_trainer import ModelTrainer
from Network_security.entity.config_entity import ModelTrainerConfig

# from Network_security.entity.config_entity import trainingpipelineconfig

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig_=trainingpipelineconfig() 
        DataIngestionConfig_=DataIngestionConfig(trainingpipelineconfig_)
        Dataingestion_=Dataingestion(DataIngestionConfig_) 
        logging.info("initiate the data ingesiton")
        dataingestionartifact=Dataingestion_.initiate_data_ingestion()
        logging.info("Data initiation completed ")
        print(dataingestionartifact
              )
        print()
        
        
        datavalidation_config=DataValidationConfig(trainingpipelineconfig_)
        data_validation=DataValidation(dataingestionartifact,datavalidation_config)
        logging.info("data validation is initiated")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation is completed")
        print(data_validation_artifact
              )
        print()
        
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig_)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("data transformation is initiated")
        data_transformation_artifact=data_transformation.initiate_data_tranformation()
        logging.info("data transformation is completed")
        print(data_transformation_artifact
              ) 
        print()
        
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig_)
        model_trainer=ModelTrainer(data_transformation_artifact,model_trainer_config) 
        logging.info("model training is initiated")
        model_trainer_artifact=model_trainer.initiate_model_training() 
        logging.info("model training iss completed")
        print(model_trainer_artifact
              )
        print() 
            
    except  Exception as e:
        raise NetworkSecurityexception(e,sys) 

    