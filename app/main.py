from werkzeug import generate_password_hash, check_password_hash
from flask import Flask, g, render_template, request, jsonify, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = b'_2#p2O"AB9ba\p\sec]/'


def get_db():
    db = getattr(g, 'sqlite_db', None)
    if db is None:
        db = g.sqlite_db = sqlite3.connect("{}/db/{}.db".format(os.getenv("APP_DIR"), os.getenv("DB_NAME")))
    return db


def init_db():
    with app.app_context():
        db = get_db()
        user_table = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';").fetchone()
        if not user_table:
            with app.open_resource('{}/db/user.sql'.format(os.getenv("APP_DIR")), mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def insert_user(user_object):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO user (user_name, user_email, user_password) VALUES (\"{}\", \"{}\", \"{}\");""".format(*user_object))
    conn.commit()
    cursor.execute("""SELECT * FROM user WHERE user_email=\"{}\";""".format(user_object[1]))
    changes = cursor.fetchone()
    cursor.close()
    return changes


@app.route("/ping")
def ping():
    return "pong"


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/showSignUp")
def showSignUp(status=200, **kwargs):
    return render_template("signup.html", **kwargs), status


@app.route("/signUp", methods=["POST"])
def signUp():
    try:
        name = request.form["inputName"]
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]

        if name and email and password:
            hashed_pwd = generate_password_hash(password, "sha256")
            user = (name, email, hashed_pwd)
            data = insert_user(user)

            if len(data) != 0:
                return render_template("signup.html", message="User created successfully !")
            else:
                return render_template("signup.html", error="Backend Error")
        else:
            error_msg = "Enter all the information"
            return render_template("signup.html", error=error_msg)

    except Exception as e:
        return render_template("signup.html", error="Error while inserting in to DB")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.sqlite_db.close()


@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
