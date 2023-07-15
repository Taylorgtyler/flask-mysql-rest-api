from flask import request, jsonify, Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the extension and the app
db = SQLAlchemy()
app = Flask(__name__)

# Load the connection string environment variable
load_dotenv()
URI = os.environ.get('MYSQL_DATABASE_URI')

# Configure the MySQL database
app.config["SQLALCHEMY_DATABASE_URI"] = URI

# Initialize the app with the extension
db.init_app(app)

# Create python classes for our tables
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Email = Column(String(100))
    DateOfBirth = Column(Date, nullable=False)
    IsAdmin = Column(Boolean, default=False, nullable=False)
    DateCreated = Column(DateTime, nullable=False)
    LastUpdated = Column(DateTime, nullable=False)

    tasks = relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.Username}', email='{self.Email}')>"

class Tasks(Base):
    __tablename__ = 'tasks'

    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    TaskTitle = Column(String(100), nullable=False)
    TaskDescription = Column(String(255), nullable=False)
    DueDate = Column(DateTime, nullable=False)
    IsComplete = Column(Boolean, default=False, nullable=False)
    DateCreated = Column(DateTime, nullable=False)
    LastUpdated = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tasks")


# Routes

## Users

### Get all users in the database
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all() 
        return make_response(jsonify([user.join() for user in users]))
    
    except Exception as e:
        return make_response(jsonify({'message': 'Oops, error getting the users'}))


### Get one user in the databse
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = Users.query.filter_by(id=id).first()

        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}), 500)


### Create a user in the database
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_jsob()
        new_user = Users(username=data['username'],
                         password=data['password'],
                         FirstName=data['firstname'],
                         LastName=data['lastname'],
                         Email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    
    except Exception as e:
        return make_response(jsonify({'message': 'oh no, error creating user'}), 500)
    
