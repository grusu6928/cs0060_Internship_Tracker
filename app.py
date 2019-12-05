#!/usr/bin/python3

from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
# TODO: add imports for database stuff
from flask_pymongo import MongoClient


app = Flask(__name__)
Bootstrap(app)

# TODO: connect to your database and create necessary tables/collections
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.internship_tracker
collection = db.login

app.config['SECRET_KEY'] = 'Blah blah blah'

todo_list = []

class NewUserForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1,64), Email()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class User:
    def __init__(self,user,password):
        self.user = users
        self.password = password

    def serialize(self):
        return {"user" : self.user, "password" : self.password}

#============================#
# Database Helper Functions! #
#============================#

def add_user(user, password):
    """Inserts a todo list item with `name` and `notes` into the database.
    Returns nothing.

    Arguments:
        name {string} -- name of todo list item
        notes {string} -- notes of todo list item
    """
    newUser = User(user,password)
    collection.insert_one(newUser)
    return


# TODO: Edit this function so that it inserts the new todo item into the database
#       and pulls most up to date todolist data from the database
@app.route('/newUser', methods=['GET', 'POST'])
def main_page():
    form = NewUserForm(method="POST")
    if form.validate_on_submit():
        user = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''
        add_user(user,password)
    return render_template('whatev.html', form=form)

app.run()