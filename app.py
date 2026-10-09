from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3, io
from datetime import datetime
import pandas as pd
from ml_model import recommend_careers

app = Flask(__name__)
app.secret_key = "change-this-before-deployment"
DB = "career_survey.db"
QUESTIONS = [
("q1","How much do you enjoy programming/coding?","Programming"),
("q2","How interested are you in building websites or web applications?","Web Development"),
("q3","How interested are you in mobile application development?","App Development"),
("q4","How much do you enjoy working with numbers, tables and Excel?","Data Analysis"),
("q5","How interested are you in statistics and finding patterns in data?","Statistics"),
("q6","How interested are you in Artificial Intelligence and Machine Learning?","AI/ML"),
("q7","How interested are you in cybersecurity and ethical hacking concepts?","Cybersecurity"),
("q8","How interested are you in networks, servers and system administration?","Networking"),
("q9","How much do you enjoy designing interfaces and user experiences?","UI/UX"),
("q10","How interested are you in solving logical/technical problems?","Problem Solving"),
("q11","How interested are you in learning Python?","Python"),
("q12","How interested are you in databases and SQL?","Database")]
ROADMAPS = {
"Web Developer":["HTML + CSS","JavaScript and responsive design","Git and GitHub","Build a portfolio website","Learn Flask/Django or React"],
"Data Analyst":["Excel and data cleaning","SQL fundamentals","Python with Pandas","Statistics and visualization","Build a dashboard project"],
"AI/ML Engineer":["Python fundamentals","Math and basic statistics","Pandas and NumPy","Scikit-learn basics","Build an ML project"],
"Cybersecurity":["Networking fundamentals","Linux basics","Security principles","Practice in legal cyber labs","Learn defensive security tools"],
"Mobile App Developer":["Programming fundamentals","Flutter or Android basics","App UI design","Connect to an API/database","Build a demo app"],
"UI/UX Designer":["Design principles","Figma basics","User research and wireframes","Prototype and usability testing","Create a portfolio case study"]}

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,age INTEGER,gender TEXT,course TEXT,year TEXT,
        q1 INTEGER,q2 INTEGER,q3 INTEGER,q4 INTEGER,q5 INTEGER,q6 INTEGER,q7 INTEGER,q8 INTEGER,q9 INTEGER,q10 INTEGER,q11 INTEGER,q12 INTEGER,
        prediction TEXT,submitted_at TEXT)""")

@app.route("/")
def index():
    return render_template("index.html", questions=QUESTIONS)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        name=request.form["name"].strip()
        age=int(request.form["age"])
        vals=[int(request.form[k]) for k,_,_ in QUESTIONS]
        if not name or not 15 <= age <= 80 or any(v not in range(1,6) for v in vals): raise ValueError
    except (ValueError,KeyError):
        flash("Complete the required details and rate every question from 1 to 5.")
        return redirect(url_for("index"))
    recs=recommend_careers(vals)
    with sqlite3.connect(DB) as c:
        c.execute("""INSERT INTO responses(name,age,gender,course,year,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,prediction,submitted_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [name,age,request.form.get("gender",""),request.form.get("course","BCA"),request.form.get("year","Second Year")]
        + vals + [recs[0]["career"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    return render_template("result.html",name=name,recommendations=recs,roadmaps=ROADMAPS)

@app.route("/dashboard")
def dashboard():
    with sqlite3.connect(DB) as c: df=pd.read_sql_query("SELECT * FROM responses ORDER BY id DESC",c)
    counts=df["prediction"].value_counts().to_dict() if not df.empty else {}
    courses=df["course"].fillna("Not specified").value_counts().to_dict() if not df.empty else {}
    return render_template("dashboard.html",total=len(df),counts=counts,courses=courses,rows=df.head(50).to_dict("records"))

@app.route("/export.csv")
def export_csv():
    with sqlite3.connect(DB) as c: df=pd.read_sql_query("SELECT * FROM responses ORDER BY id DESC",c)
    out=io.StringIO(); df.to_csv(out,index=False)
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=career_survey_results.csv"})

init_db()

if __name__ == "__main__":
    app.run(debug=True)
