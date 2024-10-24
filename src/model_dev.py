import logging
from abc import ABC, abstractmethod
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd

class Model(ABC):
    @abstractmethod
    def train(self, 
              X_train: pd.DataFrame, 
              Y_train: pd.Series,
              use_grid_search: bool = False, 
              **kwargs):
        pass    

class LogisticRegressionModel(Model):

    def train(self, 
              X_train: pd.DataFrame, 
              Y_train: pd.Series, 
              use_grid_search: bool = False, 
              **kwargs):
        try:
            if use_grid_search:
                param_grid = {
                    'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'solver': ['liblinear', 'saga'],
                    'penalty': ['l1', 'l2', 'elasticnet', None],
                }
                clf = GridSearchCV(LogisticRegression(), param_grid, 
                                   scoring='recall', cv=5)
            else:
                clf = LogisticRegression(**kwargs)

            clf.fit(X_train, Y_train)
            logging.info("Logistic Regression Model training completed")

            # Return the best estimator if grid search was used
            return clf.best_estimator_ if use_grid_search else clf
        except Exception as e:
            logging.error(f"Error in training the model: {e}")
            raise e
        
class DecisionTreeModel(Model):

    def train(self, 
              X_train: pd.DataFrame, 
              Y_train: pd.Series, 
              use_grid_search: bool = False, 
              **kwargs):
        try:
            if use_grid_search:
                param_grid = {
                    'max_depth': [None, 5, 10, 20],
                    'min_samples_split': list(range(2,12,2)),
                    'min_samples_leaf': list(range(1,5)),
                }
                clf = GridSearchCV(DecisionTreeClassifier(), param_grid, 
                                   scoring='recall', cv=5)
            else:
                clf = DecisionTreeClassifier(**kwargs)

            clf.fit(X_train, Y_train)
            logging.info("Decision Tree Model training completed")

            return clf.best_estimator_ if use_grid_search else clf
        except Exception as e:
            logging.error(f"Error in training the model: {e}")
            raise e

class RandomForestModel(Model):

    def train(self, 
              X_train: pd.DataFrame, 
              Y_train: pd.Series, 
              use_grid_search: bool = False, 
              **kwargs):
        try:
            if use_grid_search:
                param_grid = {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 5, 10, 20],
                    'min_samples_split': [2, 5, 10],
                }
                clf = GridSearchCV(RandomForestClassifier(), param_grid, 
                                   scoring='recall', cv=5)
            else:
                clf = RandomForestClassifier(**kwargs)

            clf.fit(X_train, Y_train)
            logging.info("Random Forest Model training completed")

            return clf.best_estimator_ if use_grid_search else clf
        except Exception as e:
            logging.error(f"Error in training the model: {e}")
            raise e
