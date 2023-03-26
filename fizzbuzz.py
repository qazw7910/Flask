from flask import Flask, render_template

fizzbuzz = Flask(__name__)


def divisibleby(value, other):
    return value % other == 0



@fizzbuzz.route('/')
def todo():
    return render_template("jinja2_inheritance/fizzbuzz.html")

if __name__ == '__main__':
    fizzbuzz.run(debug=True)
