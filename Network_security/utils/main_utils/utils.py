import yaml
import os,sys
# import dill
import pickle
import numpy as np

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityexception(e,sys)
    
def write_yaml_file(file_path:str,content: object, replace: bool = False )->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        os.makedirs(os.path.dirname(file_path), exist_ok=True) 
        with open(file_path,"w") as file:
            yaml.dump(content, file) 
            
    except Exception as e:
        raise NetworkSecurityexception(e,sys)   
    
def save_numpyarray_data(file_path:str, array:np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as fileobj:
            np.save(fileobj,array)
    except Exception as e:
        raise NetworkSecurityexception(e,sys)
         
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("entered the save onject method of utils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as fileobj:
            pickle.dump(obj,fileobj)
        logging.info("exited,the object is saved in a pickle file")
    except Exception as e:
        raise NetworkSecurityexception(e,sys)

def load_object(file_path:str,)->object:
    logging.info(f"loading the object from {file_path}")
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file: {file_path} doesn't exist") 
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj) 
    except Exception as e:
        raise NetworkSecurityexception(e,sys) 
    
def load_numpy_arr_data(file_path:str)->np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    logging.info(f"loading the data from {file_path}")
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityexception(e,sys) 
    
def evaluate_models(x_train,y_train,x_test,y_test,models,param):
    try:
        report={}
        for i in range (len(list(models))):
            model=list(models.values())[i]
            para=param[list(models.keys())[i]]
            
            gscv=GridSearchCV(model,para,cv=3)
            gscv.fit(x_train,y_train)
            
            model.set_params(**gscv.best_params_) 
            model.fit(x_train,y_train)
            
            y_pred_train=model.predict(x_train)
            y_pred_test=model.predict(x_test)  
            
            train_model_score=r2_score(y_train,y_pred_train) 
            test_model_score=r2_score(y_test,y_pred_test)
            
            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise NetworkSecurityexception(e,sys) 
    
    