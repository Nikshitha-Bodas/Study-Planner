from flask import Flask, render_template, request, send_file

from planner import generate_timetable
from pdf_generator import create_pdf

app = Flask(__name__)

saved_name = ""
saved_timetable = []


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    global saved_name
    global saved_timetable

    student_name = request.form["student_name"]

    number_of_subjects = int(
        request.form["number_of_subjects"]
    )

    study_hours = float(
        request.form["study_hours"]
    )

    subjects = []

    for i in range(

        1,

        number_of_subjects + 1

    ):

        subjects.append(

            {

                "name":

                request.form[f"subject{i}"],

                "exam_date":

                request.form[f"exam{i}"],

                "difficulty":

                request.form[f"difficulty{i}"]

            }

        )

    timetable = generate_timetable(

        subjects,

        study_hours

    )

    saved_name = student_name

    saved_timetable = timetable

    max_periods = max(

        len(day["schedule"])

        for day in timetable

    )

    return render_template(

        "result.html",

        name=student_name,

        timetable=timetable,

        max_periods=max_periods

    )


@app.route("/download")
def download():

    path = create_pdf(

        saved_name,

        saved_timetable

    )

    return send_file(

        path,

        as_attachment=True

    )


if __name__ == "__main__":

    app.run(

        debug=True

    )