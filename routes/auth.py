from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint("auth_bp", __name__)

# ✅ Register Route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        # ✅ Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for("auth_bp.register"))

        # ✅ Hash Password & Store in DB
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Redirecting to login...", "success")
        return redirect(url_for("auth_bp.login"))  # ✅ Redirect to login page

    return render_template("register.html")



@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Validate the user's credentials
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):  # Assuming password is hashed
            session['user'] = {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
            flash("Login successful", "success")

            # ✅ Redirect based on role
            if user.role == "admin":
                return redirect(url_for("dashboard_bp.admin_dashboard"))  # Admin Dashboard
            elif user.role == "user":
                return redirect(url_for("dashboard_bp.user_dashboard"))  # User Dashboard
            elif user.role == "guest":
                return redirect(url_for("dashboard_bp.guest_dashboard"))  # Guest Dashboard
            else:
                flash("Invalid role assigned. Contact admin.", "danger")
                return redirect(url_for("auth_bp.login"))
        
        flash("Invalid credentials, please try again", "error")
        return redirect(url_for("auth_bp.login"))

    return render_template("login.html")

# ✅ Logout Route
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth_bp.login"))
