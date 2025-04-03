from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, login_manager
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from flask_migrate import Migrate  # Import Flask-Migrate
from database import init_db
app = Flask(__name__)

# ✅ Database & Secret Key Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

# ✅ Initialize DB & Flask-Login
db.init_app(app)

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"  # Redirect to login if not authenticated

# ✅ Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")


# ✅ Home Route
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Auto-create tables if not exists
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
