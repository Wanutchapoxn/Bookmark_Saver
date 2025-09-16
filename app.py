from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from db import init_db, get_user_by_username, get_user_by_id
from routes.bookmarks import bookmarks_bp
from routes.categories import categories_bp

app = Flask(__name__)
app.secret_key = "your-secret-key"

# register blueprints
app.register_blueprint(bookmarks_bp)
app.register_blueprint(categories_bp)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User class
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    row = get_user_by_id(user_id)
    if row:
        return User(id=row[0], username=row[1], password_hash=row[2])
    return None


@app.route("/")
@login_required
def index():
    return f"Hello, {current_user.username}! <a href='/logout'>Logout</a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        row = get_user_by_username(username)
        if row:
            user = User(id=row[0], username=row[1], password_hash=row[2])
            if user.check_password(password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("index"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
