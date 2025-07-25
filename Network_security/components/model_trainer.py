import os,sys

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from Network_security.entity.config_entity import ModelTrainerConfig
from Network_security.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from Network_security.utils.main_utils.utils import save_object,load_numpy_arr_data,load_object,evaluate_models
from Network_security.utils.ml_utils.metric.classification_metrics import get_classification_score
from Network_security.utils.ml_utils.model.estimator import Networkmodel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier, 
)

import mlflow

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityexception(e,sys)
        
    def track_mlflow(self,bestmodel,classificationreport):
        with mlflow.start_run():
            f1_score=classificationreport.f1_score
            precision_score=classificationreport.precision_score
            recall_score=classificationreport.recall_score 
            
            mlflow.log_metric("f1score",f1_score)
            mlflow.log_metric("precision score",precision_score)
            mlflow.log_metric("recall score",recall_score)
            mlflow.sklearn.log_model(bestmodel,"model") 
            
            
    
    def train_model(self,x_train,y_train,x_test,y_test):
        models={
            "logistic regression":LogisticRegression(verbose=1),
            # "kneighbors classifier":KNeighborsClassifier(),
            "decision tree":DecisionTreeClassifier(),
            "adaboost":AdaBoostClassifier(),
            "gradient boosting":GradientBoostingClassifier(verbose=1),
            "random forest":RandomForestClassifier(verbose=1),
        }
        params={
            "decision tree":{
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
            # 'max_features':['sqrt','log2'],
            },
            "random forest":{
            # 'criterion':['gini', 'entropy', 'log_loss'],
            
            # 'max_features':['sqrt','log2',None],
            'n_estimators': [8,16,128,256]
            },
            "gradient boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "logistic regression":{},
            "adaboost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,64,128,256]
            }
        
        }
        
        model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models
                                            ,param=params)
        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]
        
        y_pred_train=best_model.predict(x_train)
        logging.info("getting classification score from classification metrics file")  
        classification_metric_train=get_classification_score(y_true=y_train,y_pred=y_pred_train) 
        ##tracking MLFLOW
        self.track_mlflow(best_model,classification_metric_train)
        
        y_pred_test=best_model.predict(x_test)  
        classification_metric_test=get_classification_score(y_true=y_test,y_pred=y_pred_test)
        ##tracking MLFLOW
        self.track_mlflow(best_model,classification_metric_test)  
        
        
        preprocessor=load_object(self.data_transformation_artifact.transformed_object_filepath)  
        dir_path=os.path.dirname(self.model_trainer_config.trained_model_filepath)
        os.makedirs(dir_path,exist_ok=True) 
        
        Network_model=Networkmodel(preprocessor=preprocessor,model=best_model)
        logging.info(f"saving the network model:{Network_model}") 
        save_object(self.model_trainer_config.trained_model_filepath,obj=Network_model) 
        
        ##now model saving
        logging.info(f"saving the best model:{best_model}")
        save_object("final_model/model.pkl",best_model) 
            
        modeltrainerartifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_filepath,
            train_metric_artifact=classification_metric_train,
            test_metric_artifact=classification_metric_test
        )
        
        return modeltrainerartifact
        
    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_filepath
            test_file_path=self.data_transformation_artifact.transformed_test_filepath   
               
            train_arr=load_numpy_arr_data(train_file_path)
            test_arr=load_numpy_arr_data(test_file_path)
            
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1], 
            )
            
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityexception(e,sys) 
        
        
