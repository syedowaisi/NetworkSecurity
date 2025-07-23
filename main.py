from Network_security.components.data_ingestion import Dataingestion
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.config_entity import trainingpipelineconfig

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.entity.config_entity import DataValidationConfig
from Network_security.components.data_validation import DataValidation 

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
        
        datavalidation_config=DataValidationConfig(trainingpipelineconfig_)
        data_validation=DataValidation(dataingestionartifact,datavalidation_config)
        logging.info("data validation is initiated")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation is completed")
        print(data_validation_artifact
              )
        
    except  Exception as e:
        raise NetworkSecurityexception(e,sys) 

    