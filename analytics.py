import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dataset/student_data.csv")

plt.figure(figsize=(8,5))

plt.hist(
    data["Final_Score"],
    bins=5
)

plt.title("Student Score Distribution")

plt.xlabel("Scores")

plt.ylabel("Students")

plt.savefig(
    "static/images/chart.png"
)

print("Chart Saved")