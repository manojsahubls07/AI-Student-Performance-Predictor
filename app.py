from flask import Flask, render_template, request
import pandas as pd
import joblib
import mysql.connector

app = Flask(__name__)

# ==========================
# Load Machine Learning Model
# ==========================

model = joblib.load("models/model.pkl")

# ==========================
# MySQL Database Connection
# ==========================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manoj",
    database="student_prediction"
)

cursor = conn.cursor()

# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================
# Prediction Page
# ==========================

@app.route("/predict", methods=["POST"])
def predict():

    name = request.form["name"]

    study_hours = float(request.form["study_hours"])
    attendance = float(request.form["attendance"])
    assignments = int(request.form["assignments"])
    quiz = float(request.form["quiz"])
    internal_marks = float(request.form["internal_marks"])

    sample = pd.DataFrame({
        "Study_Hours": [study_hours],
        "Attendance": [attendance],
        "Assignments": [assignments],
        "Quiz": [quiz],
        "Internal_Marks": [internal_marks]
    })

    score = model.predict(sample)[0]

    # Grade Prediction

    if score >= 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B"

    elif score >= 60:
        grade = "C"

    elif score >= 40:
        grade = "D"

    else:
        grade = "F"

    # Risk Detection

    if score >= 75:
        risk = "Low Risk"

    elif score >= 50:
        risk = "Medium Risk"

    else:
        risk = "High Risk"

    # Recommendation Engine

    if score < 50:

        recommendation = """
Increase study hours.
Improve attendance.
Submit all assignments.
Focus on weak subjects.
Practice more questions.
"""

    elif score < 75:

        recommendation = """
Improve quiz performance.
Revise regularly.
Increase study hours.
Practice previous year questions.
"""

    else:

        recommendation = """
Excellent Performance.
Maintain consistency.
Keep attending classes regularly.
Continue your current study strategy.
"""

    # ==========================
    # Save Data To MySQL
    # ==========================

    sql = """
    INSERT INTO students
    (
    name,
    study_hours,
    attendance,
    assignments,
    quiz,
    internal_marks,
    predicted_score,
    grade,
    risk_level
    )

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        name,
        study_hours,
        attendance,
        assignments,
        quiz,
        internal_marks,
        round(score, 2),
        grade,
        risk
    )

    cursor.execute(sql, values)
    conn.commit()

    return render_template(
        "result.html",
        name=name,
        score=round(score, 2),
        grade=grade,
        risk=risk,
        recommendation=recommendation
    )

# ==========================
# Student Records Page
# ==========================

@app.route("/students")
def students():

    cursor.execute("SELECT * FROM students")

    records = cursor.fetchall()

    return render_template(
        "students.html",
        students=records
    )

# ==========================
# Run Application
# ==========================

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/dashboard")
def dashboard():

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(predicted_score) FROM students"
    )

    avg_score = cursor.fetchone()[0]

    if avg_score is None:
        avg_score = 0

    avg_score = round(avg_score, 2)

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level='High Risk'"
    )

    high_risk = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_students=total_students,
        avg_score=avg_score,
        high_risk=high_risk
    )