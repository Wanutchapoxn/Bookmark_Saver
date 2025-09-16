from flask import Blueprint, request, redirect, url_for
from db import get_connection

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/add_category", methods=["POST"])
def add_category():
    new_cat = request.form["new_category"]
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (new_cat,))
        conn.commit()
    return redirect(url_for("bookmarks.index"))

@categories_bp.route("/delete_category/<name>")
def delete_category(name):
    with get_connection() as conn:
        c = conn.cursor()
        if name != "Other":
            c.execute("DELETE FROM categories WHERE name = ?", (name,))
            c.execute("UPDATE bookmarks SET category='Other' WHERE category=?", (name,))
        conn.commit()
    return redirect(url_for("bookmarks.index"))
