from datetime import datetime

from datetime import timedelta


def generate_timetable(

        subjects,

        study_hours):

    today = datetime.today()

    # ----------------

    # Exam priority

    # ----------------

    for subject in subjects:

        subject["exam"] = datetime.strptime(

            subject["exam_date"],

            "%Y-%m-%d"

        )

        days_left = (

            subject["exam"]

            -

            today

        ).days

        score = 0

        # Exam priority

        if days_left <= 2:

            score += 6

        elif days_left <= 5:

            score += 5

        elif days_left <= 10:

            score += 4

        else:

            score += 3

        # Difficulty priority

        if subject["difficulty"] == "Hard":

            score += 3

        elif subject["difficulty"] == "Medium":

            score += 2

        else:

            score += 1

        subject["score"] = score

        subject["days_left"] = days_left

    subjects.sort(

        key=lambda x:

        -x["score"]

    )

    timetable = []

    current_date = today + timedelta(

        days=1

    )

    rotation = 0

    for i in range(7):

        rotated = (

            subjects[rotation:]

            +

            subjects[:rotation]

        )

        remaining = study_hours

        schedule = []

        for subject in rotated:

            if subject["difficulty"] == "Hard":

                if subject["days_left"] <= 3:

                    hrs = 2.5

                else:

                    hrs = 2

            elif subject["difficulty"] == "Medium":

                if subject["days_left"] <= 3:

                    hrs = 2

                else:

                    hrs = 1.5

            else:

                if subject["days_left"] <= 3:

                    hrs = 1.5

                else:

                    hrs = 1

            if hrs <= remaining:

                schedule.append(

                    {

                        "subject":

                        subject["name"],

                        "hours":

                        hrs

                    }

                )

                remaining -= hrs

        if remaining > 0:

            schedule.append(

                {

                    "subject":

                    "Revision / Practice Questions",

                    "hours":

                    round(

                        remaining,

                        1

                    )

                }

            )

        timetable.append(

            {

                "day":

                current_date.strftime(

                    "%A"

                ),

                "date":

                current_date.strftime(

                    "%d-%m-%Y"

                ),

                "schedule":

                schedule

            }

        )

        current_date += timedelta(

            days=1

        )

        rotation += 1

        if rotation == len(subjects):

            rotation = 0

    return timetable