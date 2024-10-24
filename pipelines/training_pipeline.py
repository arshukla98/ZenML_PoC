from zenml import pipeline
from steps.clean_data import clean_df
from steps.evaluation import evaluate_model
from steps.ingest_data import ingest_df
from steps.model_train import train_model

@pipeline(enable_cache=False)
def train_pipeline(data_path:str):

    df = ingest_df(data_path=data_path)
    
    X_train,X_test,Y_train,Y_test = clean_df(df)

    model = train_model(X_train, Y_train)
    
    evaluation_metrics = evaluate_model(model,X_test,Y_test)
