from zenml.steps import BaseParameters

class ModelNameConfig(BaseParameters):
    model_name: str="DecisionTree" # LogisticRegression, DecisionTree, RandomForest