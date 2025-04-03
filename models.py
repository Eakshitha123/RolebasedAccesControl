from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime

# Initialize the database instance
db = SQLAlchemy()
login_manager = LoginManager()

# User model
class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed Password
    role = db.Column(db.String(20), nullable=False)  # admin/user/guest

    # Define the relationship with File model (One-to-Many)
    #files = db.relationship('File', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Track which user uploaded
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, filename, filepath, user_id):
        self.filename = filename
        self.filepath = filepath
        self.user_id = user_id

# ✅ Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# File model
#class File(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #filename = db.Column(db.String(100), nullable=False)
    #filepath = db.Column(db.String(200), nullable=False)  # Ensure filepath is defined
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key reference to User's id

    # No need to redefine `user` here because backref in User model already does that.
    # user = db.relationship('User', backref=db.backref('files', lazy=True)) # This line is not needed.

    #def __repr__(self):
        #return f'<File {self.filename}>'
