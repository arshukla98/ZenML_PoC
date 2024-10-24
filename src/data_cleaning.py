import logging
import warnings
import pandas as pd
from abc import ABC, abstractmethod

from typing import Union 

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

class DataStrategy(ABC):

    @abstractmethod
    def handle_data(self, 
        data: pd.DataFrame) -> pd.DataFrame :
        pass 

class DataPreProcessStrategy(DataStrategy):
    """
    This class is used to preprocess the given dataset.
    """

    def __init__(self, encoder=None):
        self.encoder = encoder

    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            warnings.filterwarnings('ignore')
            print("Column Names Before Preprocessing:", data.columns)  # Add this line
            # data = data.drop(["EmployeeCount", "EmployeeNumber", "StandardHours"], axis=1)
            
            # if 'Attrition' in data.columns:
            #     print("Attrition column found in data.")
            # else:
            #     print("Attrition column not found in data.")

            # data["Attrition"] = data["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)
            # # data["Over18"] = data["Over18"].apply(lambda x: 1 if x == "Yes" else 0)
            # data["OverTime"] = data["OverTime"].apply(lambda x: 1 if x == "Yes" else 0)

            # # Extract categorical variables
            # cat = data[['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]

            # # Perform one-hot encoding on categorical variables
            # onehot = OneHotEncoder()
            # cat_encoded = onehot.fit_transform(cat).toarray()
            
            # #to have the feature unqiue data as their respective encoded column names
            # feature_names = onehot.get_feature_names_out(input_features=cat.columns)
            
            # # Convert cat_encoded to DataFrame
            # cat_df = pd.DataFrame(cat_encoded, columns=feature_names)
            
            # # Convert cat_encoded to DataFrame
            # cat_df = pd.DataFrame(cat_encoded)

            data["Attrition"] = data["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)
            data["OverTime"] = data["OverTime"].apply(lambda x: 1 if x == "Yes" else 0)

            numerical = data[['Age', 'Attrition', 'DistanceFromHome', 'Education', 
                              'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel', 
                              'JobSatisfaction', 'MonthlyIncome', 'NumCompaniesWorked', 
                              'OverTime', 'PercentSalaryHike', 'PerformanceRating', 
                              'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 
                              'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole', 
                              'YearsSinceLastPromotion', 'YearsWithCurrManager']]

            # data = pd.concat([numerical], axis=1)

            print("Column Names After Preprocessing:", numerical.columns)  # Add this line
            print("Preprocessed Data:")
            print(numerical.head())
            return numerical
        except Exception as e:
            logging.error(f"Error in preprocessing the data: {e}")
            raise e
        
class DataDivideStrategy(DataStrategy):

    def handle_data(self, 
                    data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        try:
            warnings.filterwarnings('ignore')
            # Check if 'Attrition' is present in the data
            if 'Attrition' in data.columns:
                X = data.drop(['Attrition'], axis=1)
                Y = data['Attrition']
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
                return X_train, X_test, Y_train, Y_test
            else:
                raise ValueError("'Attrition' column not found in data.")
        except Exception as e:
            logging.error(f"Error in data handling: {str(e)}")
            raise e

class DataCleaning:
    def __init__(self,data:pd.DataFrame,strategy:DataStrategy)->None:
        self.data=data
        self.strategy=strategy
            
    def handle_data(self)->Union[pd.DataFrame,pd.Series]:
        try:
            return self.strategy.handle_data(self.data)
        except Exception as e:
            logging.error(f"There is a error in dataHandling{e}")
            raise e