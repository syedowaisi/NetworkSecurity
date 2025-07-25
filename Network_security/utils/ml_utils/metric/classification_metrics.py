import os,sys

from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging

from sklearn.metrics import f1_score,recall_score,precision_score 
from Network_security.entity.artifact_entity import ClassificationMetricArtifact

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred) 
        
        classification_metric=ClassificationMetricArtifact(
            f1_score=model_f1_score,
            recall_score=model_recall_score,
            precision_score=model_precision_score
        )
        
        return classification_metric 
    except Exception as e:
        raise NetworkSecurityexception(e,sys) 
        