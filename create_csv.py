import pandas as pd

# Load the dataset
file_path = 'data/HR-Employee-Attrition.csv'
data = pd.read_csv(file_path)

# Select relevant columns for employee attrition prediction
selected_columns = [
    'Age', 'Attrition', 'DistanceFromHome', 'Education',
    'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 
    'MonthlyIncome', 'NumCompaniesWorked', 'OverTime', 'PercentSalaryHike', 
    'PerformanceRating', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 
    'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 
    'YearsWithCurrManager'
] 

# Filter the dataset to only include selected columns
minimized_dataset = data[selected_columns]

# Save the minimized dataset to a new CSV file
minimized_file_path = 'data/HR-Employee-Attrition-1.csv'
minimized_dataset.to_csv(minimized_file_path, index=False)

# print(minimized_dataset.head())

print(f'Minimized dataset saved to {minimized_file_path}')