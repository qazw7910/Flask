import datetime
from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for

habit = Flask(__name__)
habits = ["Test habit"]
completions = defaultdict(list)


@habit.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        date = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return date

    return {"date_range": date_range}


@habit.route("/")
def index():
    date_str = request.args.get('date')
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()

    return render_template("habit/index.html",
                           habits=habits,
                           title="Habit Tracker - Home",
                           selected_date=selected_date,
                           completions=completions[selected_date], )


@habit.route("/add", methods=['POST', 'GET'])
def add_habit():
    if request.method == 'POST':
        habits.append(request.form.get('habit'))
        print(request.form.get('habit'))
    return render_template("habit/add_habit.html", title="Habit Tracker - Add Habit")


@habit.route("/complete", methods=['POST'])
def complete():
    date_string = request.form.get('date')
    date = datetime.date.fromisoformat(date_string)
    habit = request.form.get('habitName')
    completions[date].append(habit)

    return redirect(url_for("index", date=date_string))


if __name__ == '__main__':
    habit.run(debug=True)
