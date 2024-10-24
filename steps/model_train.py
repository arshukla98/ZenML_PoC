import mlflow
import pandas as pd
import logging
from zenml import step
from src.model_dev import LogisticRegressionModel, DecisionTreeModel, RandomForestModel
from .config import ModelNameConfig
from sklearn.base import ClassifierMixin 
from zenml.client import Client

experiment_tracker = Client().active_stack.experiment_tracker

@step(experiment_tracker=experiment_tracker.name, enable_cache=False)
def train_model(
    X_train: pd.DataFrame,
    Y_train: pd.Series,
    config: ModelNameConfig,
) -> ClassifierMixin:
    try:
        model = None
        mlflow.sklearn.autolog()
        if config.model_name == "LogisticRegression":
            model = LogisticRegressionModel()
        elif config.model_name == "DecisionTree":
            model = DecisionTreeModel()
        elif config.model_name == "RandomForest":
            model = RandomForestModel()
        else:
            raise ValueError(f"Model {config.model_name} is not supported")
        
        # models = [LogisticRegressionModel(), DecisionTreeModel(), RandomForestModel()]
        # for model in models:
        #     trained_model = model.train(X_train, Y_train, True)
        
        trained_model = model.train(X_train, Y_train, True)
        return trained_model
    except Exception as e:
        logging.error(f"Error in training the model: {e}")
        raise e