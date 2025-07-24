import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer  
from sklearn.pipeline import Pipeline

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.entity.artifact_entity import DataTransformationArtifact,DatavalidationArtifact
from Network_security.entity.config_entity import DataTransformationConfig  ##,DataValidationConfig

from Network_security.utils.main_utils.utils import save_numpyarray_data,save_object
from Network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMETERS,TARGET_NAME 

class DataTransformation:
    def __init__(self,data_validation_artifact:DatavalidationArtifact,
                data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config 
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame: 
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def data_transformer_object(clf)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMETERS) ##it handles missing values
            logging.info(f"initialize knn imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMETERS}")
            
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
    def initiate_data_tranformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("starting data transformation") 
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ##training df
            input_train_feature=train_df.drop(columns=[TARGET_NAME])
            target_train_feature=train_df[TARGET_NAME]
            target_train_feature=target_train_feature.replace(-1,0)
            ##testing df
            input_test_feature=test_df.drop(columns=[TARGET_NAME])
            target_test_feature=test_df[TARGET_NAME]
            target_test_feature=target_test_feature.replace(-1,0)
            
            preprocessor=self.data_transformer_object()
            
            preprocessor_object=preprocessor.fit(input_train_feature)
            transformed_input_train_feature=preprocessor_object.transform(input_train_feature)
            transformed_input_test_feature=preprocessor_object.transform(input_test_feature)
            
            train_arr=np.c_[transformed_input_train_feature,np.array(target_train_feature)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_test_feature)]
            
            #save array data
            save_numpyarray_data(self.data_transformation_config.transformed_train_filepath,train_arr,)
            save_numpyarray_data(self.data_transformation_config.transformed_test_filepath,test_arr,)
            save_object(self.data_transformation_config.transformed_object_filepath,preprocessor,)
            
            save_object("final_model/preprocessor.pkl",preprocessor_object,)
            
            #preparing artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_filepath=self.data_transformation_config.transformed_object_filepath,
                transformed_train_filepath=self.data_transformation_config.transformed_train_filepath,
                transformed_test_filepath=self.data_transformation_config.transformed_test_filepath
            )
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 