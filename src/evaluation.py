import logging
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from abc import ABC, abstractmethod

class Evaluation(ABC):
    """
        Abstract Class defining strategy for
        evaluating our models.
    """
    @abstractmethod
    def calculate_score(self, 
                        y_true: np.ndarray,
                        y_pred: np.ndarray):
        pass

class ClassificationReport(Evaluation):
    
    def calculate_score(self, 
                        y_true: np.ndarray, 
                        y_pred: np.ndarray):
        try:
            logging.info("Confusion Matrix")
            cfMatrix = confusion_matrix(y_true, y_pred)
            print(cfMatrix)
            logging.info("Calculate Classification Report")
            report = classification_report(y_true, y_pred, output_dict=True)
            logging.info(f"Classification Report:\n{report}")
            return report
        except Exception as e:
            logging.error(f"Error in calculating Classification Report: {e}")
            raise e