import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")

        try:
            day = int(request.form.get("day"))
            month = int(request.form.get("month"))
        except:
            day = 0
            month = 0

        if not name or (day < 1 or day > 31) or (month < 1 or month > 12):

            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():

    deleteId = int(request.form.get("delete"))

    db.execute("DELETE FROM birthdays WHERE id = ?", deleteId)

    return redirect("/")


@app.route("/change", methods=["POST"])
def change():

    try:
        changeMonth = int(request.form.get("changeMonth"))
        changeDay = int(request.form.get("changeDay"))
    except:
        changeMonth = 0
        changeDay = 0

    changeId = int(request.form.get("change"))

    if (changeDay < 1 or changeDay > 31) or (changeMonth < 1 or changeMonth > 12):

        return redirect("/")

    db.execute("UPDATE birthdays SET month = ?, day = ? WHERE id = ?", changeMonth, changeDay, changeId)

    return redirect("/")
