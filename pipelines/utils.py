import logging
import pandas as pd
from src.data_cleaning import DataCleaning, DataPreProcessStrategy

def get_data_for_test():
    try:
        df = pd.read_csv("./data/HR-Employee-Attrition-1.csv")
        
        # print("Original Data sample:")
        # print(df.head())

        # Create a DataPreProcessStrategy instance with encoder
        preprocess_strategy = DataPreProcessStrategy() 

        # Data cleaning with preprocessing
        data_cleaning = DataCleaning(df, preprocess_strategy)
        df = data_cleaning.handle_data()
        
        # print("Preprocessed Data:")
        # print(df.head())
        
        df[df['Attrition'] == 1].to_csv('data/att1.csv')
        df[df['Attrition'] == 0].to_csv('data/att0.csv')
        
        # print(df[df['Attrition'] == 1].shape, df[df['Attrition'] == 0].shape) (237, 21) (1233, 21)
        
        # Drop 'Attrition' column from test data
        df.drop(["Attrition"], axis=1, inplace=True)
        
        # print("Data Shape for Inference:", df.shape)  # Data Shape for Inference: (1470, 20)

        df = df.sample(100)

        result = df.to_json(orient="split")
        return result
    except Exception as e:
        logging.error(e)
        raise e