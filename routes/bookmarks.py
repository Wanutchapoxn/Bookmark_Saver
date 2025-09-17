from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from datetime import datetime
from db import get_connection

bookmarks_bp = Blueprint("bookmarks", __name__)

@bookmarks_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    search = request.args.get("search", "")

    if request.method == "POST":
        title = request.form["title"]
        url = request.form["url"]
        category = request.form["category"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO bookmarks (title, url, category, created_at, user_id) VALUES (?, ?, ?, ?, ?)",
                      (title, url, category, created_at, current_user.id))
            conn.commit()
        return redirect(url_for("bookmarks.index"))

    with get_connection() as conn:
        c = conn.cursor()
        # ดึง category ทั้งหมด
        c.execute("SELECT name FROM categories ORDER BY name")
        categories = [row[0] for row in c.fetchall()]

        # ดึง bookmark (มี search หรือไม่)
        if search:
            c.execute("SELECT id, title, url, category, created_at FROM bookmarks WHERE user_id=? AND title  LIKE ? ORDER BY id DESC",
                      (current_user.id,'%' + search + '%',))   #ถ้าเกิดอะไรขึ้นอาจเพราะไอ่นี่แถวนี้
        else:
            c.execute("SELECT id, title, url, category, created_at FROM bookmarks  WHERE user_id=? ORDER BY id DESC",
            (current_user.id,))
        bookmarks = c.fetchall()

    return render_template("index.html", bookmarks=bookmarks, categories=categories, search=search)

@bookmarks_bp.route("/delete/<int:bookmark_id>")
def delete(bookmark_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()
    return redirect(url_for("bookmarks.index"))
