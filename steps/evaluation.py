import pickle
import mlflow

from zenml import step
import pandas as pd
from sklearn.base import ClassifierMixin
import logging

from typing import Tuple
from typing_extensions import Annotated
from src.evaluation import ClassificationReport 
from zenml.client import Client

experiment_tracker=Client().active_stack.experiment_tracker

@step(experiment_tracker=experiment_tracker.name)
def evaluate_model(model: ClassifierMixin,
                   X_test: pd.DataFrame,
                   Y_test: pd.Series) -> Annotated[float, "classification_report"]:
    try:
        prediction = model.predict(X_test)
        report_class = ClassificationReport()  # Create an instance of ClassificationReport
        report = report_class.calculate_score(Y_test, prediction)
        
        # Log individual metrics
        mlflow.log_metrics({
            "precision_0": report["0"]["precision"],
            "recall_0": report["0"]["recall"],
            "f1_score_0": report["0"]["f1-score"],
            "precision_1": report["1"]["precision"],
            "recall_1": report["1"]["recall"],
            "f1_score_1": report["1"]["f1-score"],
            "accuracy": report["accuracy"],
        })
        
        # Save the model to a file
        with open('saved_model/model.pkl', 'wb') as file:
            pickle.dump(model, file)

        return report["accuracy"]
    except Exception as e:
        logging.error(f"Error in evaluating the model: {e}")
        raise e