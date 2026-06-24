import pandas as pd

data = pd.read_csv("dataset/student_data.csv")

print(data.head())

print(data.info())

print(data.describe())