from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(student_name, timetable):

    filename = "StudyPlanner.pdf"

    document = SimpleDocTemplate(filename)

    elements = []

    styles = getSampleStyleSheet()

    title = Paragraph(

        f"<b>{student_name}'s Weekly Timetable</b>",

        styles["Title"]

    )

    elements.append(title)

    elements.append(Spacer(1, 10))

    max_periods = max(

        len(day["schedule"])

        for day in timetable

    )

    headers = ["Day"]

    for i in range(max_periods):

        headers.append(

            f"Period {i+1}"

        )

    data = [headers]

    for day in timetable:

        row = []

        row.append(

            f"{day['day']}\n{day['date']}"

        )

        for item in day["schedule"]:

            row.append(

                f"{item['subject']}\n({item['hours']} hrs)"

            )

        while len(row) < max_periods + 1:

            row.append("-")

        data.append(row)

    table = Table(data)

    table.setStyle(

        TableStyle([

            (

                "GRID",

                (0,0),

                (-1,-1),

                1,

                colors.black

            ),

            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.lightgrey

            ),

            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            ),

            (

                "VALIGN",

                (0,0),

                (-1,-1),

                "MIDDLE"

            )

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 15))

    note = Paragraph(

        "<b>Note:</b> If time remains, revise previously studied topics or practice a short mock test.",

        styles["Normal"]

    )

    elements.append(note)

    document.build(elements)

    return filename