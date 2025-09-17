from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from db import init_db, get_user_by_username, get_user_by_id, create_user
from routes.bookmarks import bookmarks_bp
from routes.categories import categories_bp

app = Flask(__name__)
app.secret_key = "your-secret-key"

init_db()

#  register blueprints
app.register_blueprint(bookmarks_bp)
app.register_blueprint(categories_bp)

# Login Manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"   # ถ้า user ยังไม่ login → redirect ไป /login


# ===== User Class =====
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


# ===== Routes =====
@app.route("/")
def home():
    """เมื่อเปิดเว็บครั้งแรกให้ redirect ไปหน้า login"""
    if current_user.is_authenticated:
        return redirect(url_for("bookmarks.index"))
    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        row = get_user_by_username(username)
        if row:
            user = User(id=row[0], username=row[1], password_hash=row[2])
            if user.check_password(password):
                login_user(user)
                flash("Login successful!", "success")
                # 🔑 หลัง login เสร็จไปที่หน้า bookmark หลัก
                return redirect(url_for("bookmarks.index"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_created = create_user(username, password)
        if user_created:
            row = get_user_by_username(username)
            user = User(id=row[0], username=row[1], password_hash=row[2])
            login_user(user)
            flash("Registration successful! You are now logged in.", "success")
            # 🔑 หลัง register เสร็จไปที่หน้า bookmark หลัก
            return redirect(url_for("bookmarks.index"))
        else:
            flash("Username already exists.", "danger")

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
