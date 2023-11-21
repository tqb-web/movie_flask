from flask import Blueprint, jsonify, request
import sqlite3
from flask_login import current_user

user_validation_bp = Blueprint('user_validation', __name__)


@user_validation_bp.route("/check_username", methods=["POST"])
def check_username():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@user_validation_bp.route("/check_username_afterLogin", methods=["POST"])
def check_username_afterLogin():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    cursor = db.cursor()
    cursor.execute('select * from usertable where username = ? and id != ?', (username, current_user.userid))
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@user_validation_bp.route("/check_phone", methods=["POST"])
def check_phone():
    db = sqlite3.connect("database/userInfo.db")
    phone = request.form["phone"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE phone=?"
    params = (phone,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@user_validation_bp.route("/check_email", methods=["POST"])
def check_email():
    db = sqlite3.connect("database/userInfo.db")
    email = request.form["email"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE email=?"
    params = (email,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})
