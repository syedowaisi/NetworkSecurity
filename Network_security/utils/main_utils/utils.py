import yaml
import os,sys
# import dill
import pickle
import numpy as np

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

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
    