import pandas as pd
import joblib

model = joblib.load("models/model.pkl")

sample = pd.DataFrame({
    "Study_Hours": [5],
    "Attendance": [80],
    "Assignments": [8],
    "Quiz": [75],
    "Internal_Marks": [78]
})

prediction = model.predict(sample)

print("Predicted Score:", round(prediction[0], 2))