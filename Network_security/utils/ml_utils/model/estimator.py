import os,sys 

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class Networkmodel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_prediction=self.model.predict(x_transform)
            return y_prediction    
        except Exception as e:
            raise NetworkSecurityexception(e,sys)     
        
        