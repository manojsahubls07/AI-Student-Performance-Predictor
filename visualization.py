import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dataset/student_data.csv")

plt.figure(figsize=(8,5))

plt.scatter(
    data["Study_Hours"],
    data["Final_Score"]
)

plt.title("Study Hours vs Final Score")
plt.xlabel("Study Hours")
plt.ylabel("Final Score")

plt.grid(True)

plt.show()