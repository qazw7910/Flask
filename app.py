import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI"))
app.db = client.microblog

todos = [
    ("Get milk", False),
    ("Learn programming", True)
]

@app.route("/", methods=["GET", "POST"])
def home():
    print([e for e in app.db.entries.find({})])

    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_datetime = datetime.now().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_datetime})

    entries_with_date = [(entry["content"], entry["date"], entry["date"]) for entry in app.db.entries.find({})]
    return render_template('home.html', entries=entries_with_date)


@app.route("/todo/")
def todo():
    return render_template("jinja2_inheritance/jinja_lab.html", todos=todos)

@app.route("/todo/<string:todo>")
def todo_item(todo:str):
    for text, completed in todos:
        if text == todo:
            completed_text = "[x]" if completed else "[]"
            title = f"{completed_text} - Todos"
            return render_template("jinja2_inheritance/todo.html", text=text, completed=completed, title=title)
    else:
        return render_template("jinja2_inheritance/not-found.html", text=todo, title="Not found")


@app.route("/expression/")
def render_expression():
    # interpolation
    color = "brown"
    animal_one = "fox"
    animal_two = "dog"

    # addition and subtraction
    orange_amount = 10
    apple_amount = 20
    donate_amount = 15

    # string concatenation
    first_name = "Captain"
    last_name = "Marvel"

    kwargs = {
        "color": color,
        "animal_one": animal_one,
        "animal_two": animal_two,
        "orange_amount": orange_amount,
        "apple_amount": apple_amount,
        "donate_amount": donate_amount,
        "first_name": first_name,
        "last_name": last_name
    }
    return render_template(
        "expressions.html", **kwargs
    )


class GalileanMoons:
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


@app.route("/data-structures/")
def render_data_structures():
    movies = [
        "Leon the Professional",
        "The Usual Suspects",
        "A Beautiful Mind"
    ]
    car = {
        "brand": "Tesla",
        "model": "Roadster",
        "year": "2020",
    }
    moons = GalileanMoons("Io", "Europa", "Ganymede", "Callisto")

    kwargs = {
        "movies": movies,
        "car": car,
        "moons": moons
    }

    return render_template(
        "data_structures.html", **kwargs
    )


@app.route("/conditionals-basics/")
def render_conditionals_basics():
    company = "Apple"
    return render_template("conditionals_basics.html", company=company)


@app.route("/for-loop/")
def render_for_loop():
    planets = [
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupyter",
        "Saturn",
        "Uranus",
        "Neptune",
    ]
    return render_template("for_loop.html", planets=planets)


@app.route("/for-loop/dict/")
def render_for_loop_dict():
    cuisines = {
        "Italy": "Neapolitan Pizza",
        "France": "Baguette",
        "Spain": "Churros",
        "Japan": "Sushi",
        "India": "Dosa",
    }
    return render_template("for_loop_dict.html", cuisines=cuisines)


@app.route("/for-loop/conditionals")
def for_loop_conditionals():
    user_os = [
        ("Miller", "Windows"),
        ("Bob", "MacOS"),
        ("Zach", "Linux"),
        ("Annie", "Linux"),
        ("Farah", "Windows"),
        ("George", "Windows"),
    ]
    return render_template("for_loop_conditionals.html", user_os=user_os)


if __name__ == '__main__':
    app.run(debug=True)
