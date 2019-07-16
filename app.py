import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import lookup


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/explore", methods=["GET", "POST"])
def explore():
    books = []
    if request.method == "POST":
        searchTerm = request.form.get("booksearch")
        print(searchTerm)
        jsonresult = lookup(searchTerm)
        books = []
        for j in jsonresult:
            books.append(j['volumeInfo'])
        for book in books:
            if book.get('imageLinks') == None:
                book['imageLinks'] = {'smallThumbnail':"https://dhmckee.com/wp-content/uploads/2018/11/defbookcover-min.jpg"}
            if book.get('authors') == None:
                book['authors'] = ["N/A"]
        return render_template('explore.html',books=books)
    return render_template("explore.html")


@app.route("/bestseller")
def bestseller():
    return render_template("best.html")


@app.route("/quote")
def quote():
    return render_template("quotes.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        sql = "SELECT * FROM readers;"
        abc = db.execute(sql).fetchall()
        print(abc)
        return render_template(
            "home.html",
            username=username,
            name=name,
            email=email,
            password=password,
            confirm=confirm,
        )
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/home", methods=["POST"])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
