import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from flask_session import Session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import lookup, apology, login_required


# configure application
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# ensure response aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if not session.get("user_id") is None:
        rows = db.execute(
            text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
        ).fetchall()
        name = rows[0]["name"]
        return render_template("index.html", name=name)
    else:
        return render_template("index.html")


@app.route("/explore", methods=["GET", "POST"])
def explore():
    if request.method == "POST":
        searchTerm = request.form.get("booksearch")
        jsonresult = lookup(searchTerm)
        books = []
        for j in jsonresult:
            books.append(j["volumeInfo"])
        for book in books:
            # book["imageLinks"]["smallThumbnail"] = book["imageLinks"]["smallThumbnail"].replace("http","https")
            if book.get("imageLinks") == None:
                book["imageLinks"] = {
                    "smallThumbnail": "https://dhmckee.com/wp-content/uploads/2018/11/defbookcover-min.jpg"
                }
            if book.get("authors") == None:
                book["authors"] = ["N/A"]
            if book.get("averageRating") == None:
                book["averageRating"] = 0
        if not session.get("user_id") is None:
            rows = db.execute(
                text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
            ).fetchall()
            db.close()
            name = rows[0]["name"]
            return render_template("explore.html", books=books, name=name)
        else:
            return render_template("explore.html", books=books)
    else:
        if not session.get("user_id") is None:
            rows = db.execute(
                text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
            ).fetchall()
            db.close()
            name = rows[0]["name"]
            return render_template("explore.html", name=name)
        else:
            return render_template("explore.html")


@app.route("/bestseller")
def bestseller():
    if not session.get("user_id") is None:
        rows = db.execute(
            text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
        ).fetchall()
        db.close()
        name = rows[0]["name"]
        return render_template("best.html", name=name)
    else:
        return render_template("best.html")


@app.route("/shelf")
def shelf():
    if not session.get("user_id") is None:
        rows = db.execute(
            text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
        ).fetchall()
        db.close()
        name = rows[0]["name"]
        shelf = db.execute(
            text("SELECT * FROM shelf WHERE id = :id"), {"id": session["user_id"]}
        ).fetchall()
        db.close()
        return render_template("shelf.html", name=name, shelf=shelf)
    else:
        return render_template("shelf.html")


@app.route("/quote")
def quote():
    if not session.get("user_id") is None:
        rows = db.execute(
            text("SELECT * FROM readers WHERE id = :id"), {"id": session["user_id"]}
        ).fetchall()
        db.close()
        name = rows[0]["name"]
        return render_template("quotes.html", name=name)
    else:
        return render_template("quotes.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # ensure user has entered usernamae
        if not request.form.get("username"):
            return apology("Missing username", 400)

        # ensure user enters name
        elif not request.form.get("name"):
            return apology("Please Enter Your Name", 400)

        # ensure user enters email
        elif not request.form.get("email"):
            return apology("Please Enter Your Email", 400)

        # ensure user enters password
        elif not request.form.get("password"):
            return apology("Please Enter Your Name", 400)

        # ensure passwords match
        elif not request.form.get("password") == request.form.get("confirm"):
            return apology("Passwords should Match", 400)

        # hashing the password
        password = generate_password_hash(request.form.get("password"))

        result = db.execute(
            text(
                "INSERT INTO readers (username,name, email, password) VALUES(:username,:name,:email,:password)"
            ),
            {
                "username": request.form.get("username"),
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "password": password,
            },
        )
        db.commit()
        db.close()
        if not result:
            return apology("Username already exists", 400)

        rows = db.execute(
            text("SELECT * FROM readers WHERE username = :username"),
            {"username": request.form.get("username")},
        ).fetchall()
        db.close()
        session["user_id"] = rows[0]["id"]
        name = rows[0]["name"]
        return redirect(url_for("index", name=name))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # clearing the session so that no one is logged in
    session.clear()

    # user makes a post request
    if request.method == "POST":

        # ensure user enters username
        if not request.form.get("user"):
            return apology("Missing username", 400)

        # ensure user enters username
        if not request.form.get("password"):
            return apology("Missing password", 400)

        # query datatbase for data
        rows = db.execute(
            text("SELECT * FROM readers WHERE username = :username"),
            {"username": request.form.get("user")},
        ).fetchall()

        # ensure login data exists in database
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

        # remember the user who has logged in
        session["user_id"] = rows[0]["id"]
        name = rows[0]["name"]
        # redirect user to home page
        return redirect(url_for("index", name=name))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["POST"])
def add():
    if not session.get("user_id") is None:
        # ensure user enter book title
        if not request.form.get("title"):
            return apology("Missing book title", 400)

        elif not request.form.get("author"):
            return apology("Missing author", 400)

        elif not request.form.get("pages"):
            return apology("Missing of pages", 400)

        elif not request.form.get("shelf"):
            return apology("Missing Book Shelf", 400)

        rating = request.form.get("rating")
        result = db.execute(
            text(
                "INSERT INTO shelf (id,title, author, pages, shelf, rating) VALUES(:id,:title,:author,:pages,:shelf, :rating)"
            ),
            {
                "id": session["user_id"],
                "title": request.form.get("title"),
                "author": request.form.get("author"),
                "pages": request.form.get("pages"),
                "shelf": request.form.get("shelf"),
                "rating": rating,
            },
        )
        db.commit()
        flash("Book Added")
        db.close()

        return redirect(url_for("shelf"))
    else:
        return apology("You need to be Logged In to add book", 400)


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("book-to-remove")
    db.execute(text("DELETE FROM shelf where title = :title"), {"title": title})
    db.commit()
    db.close()
    return redirect(url_for("shelf"))

@app.route("/offline.html")
def offline():
    return app.send_static_file("offline.html")

@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file("sw.js")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=8080)
