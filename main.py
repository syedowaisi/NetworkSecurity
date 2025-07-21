from Network_security.components.data_ingestion import Dataingestion
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.config_entity import trainingpipelineconfig

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

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
        
    except  Exception as e:
        raise NetworkSecurityexception(e,sys) 

    