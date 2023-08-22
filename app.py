from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

users_database = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        users_database[username] = hashed_password
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        if username in users_database and bcrypt.checkpw(password, users_database[username]):
            session["username"] = username
            return redirect(url_for("secured"))
    return render_template("login.html")

@app.route("/secured")
def secured():
    if "username" in session:
        return "Welcome to the secured page, {}!".format(session["username"])
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
