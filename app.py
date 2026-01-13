
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="137537ca.",
        database="hospital"
    )

@app.route("/")
def dashboard():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM doctors")
    doctors = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM patients")
    patients = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM appointments")
    appointments = cur.fetchone()[0]
    con.close()
    return render_template("dashboard.html", doctors=doctors, patients=patients, appointments=appointments)

@app.route("/doctors")
def doctors():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM doctors")
    data = cur.fetchall()
    con.close()
    return render_template("doctors.html", doctors=data)

@app.route("/patients")
def patients():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    con.close()
    return render_template("patients.html", patients=data)

@app.route("/appointments", methods=["GET","POST"])
def appointments():
    con = get_connection()
    cur = con.cursor()
    if request.method == "POST":
        cur.execute(
            "INSERT INTO appointments (patientName, doctorName, _date, duration, amountPaid) VALUES (%s,%s,CURDATE(),%s,%s)",
            (
                request.form["patient"],
                request.form["doctor"],
                int(request.form["duration"]),
                int(request.form["duration"]) * 100
            )
        )
        con.commit()
        return redirect(url_for("appointments"))
    cur.execute("SELECT * FROM appointments")
    data = cur.fetchall()
    con.close()
    return render_template("appointments.html", appointments=data)

if __name__ == "__main__":
    app.run(debug=True)
