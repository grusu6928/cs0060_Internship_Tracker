import os

from flask import Flask
from flask import render_template, redirect, request, url_for, flash, session

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_table import Table, Col

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class LoginForm(FlaskForm):
    email_or_user = StringField('Email or username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Register')

class InternshipForm(FlaskForm):
    company = StringField('Company', [DataRequired()])
    medium = StringField('Medium')
    position = StringField('Position')
    location = StringField('Location')
    notes = StringField('Notes')
    documents = StringField('Documents')
    status = SelectField('Status', choices=[
            ('none',''),
            ('watch_list', 'watch/follow up'), 
            ('not_applicable', 'no longer applicable'), 
            ('received_offer', 'received offer')])
    submit = SubmitField('Submit')
    
class InternshipTable(Table):
    classes = ['table', 'table-hover']
    company = Col('Company')
    medium = Col('Medium')
    position = Col('Position')
    location = Col('Location')
    notes = Col('Notes')
    documents = Col('Documents')
    def get_tr_attrs(self, internship):
        if internship.watch_list():
            return {'class': 'warning'}
        if internship.not_applicable():
            return {'class': 'info'}
        if internship.received_offer():
            return {'class': 'success'}
        else:
            return {}
        
class Internship(object):
    def __init__(self, _id, user_id, company, medium=None, position=None, \
                 location=None, notes=None, documents=None, status=None):
        self._id = _id
        self.user_id = user_id
        self.company = company
        self.medium = medium
        self.position = position
        self.location = location
        self.notes = notes
        self.documents = documents
        self.status = status
    def watch_list(self):
        return self.status == 'watch_list'
    def not_applicable(self):
        return self.status == 'not_applicable'
    def received_offer(self):
        return self.status == 'received_offer'
    

# make sure app secret exists
# generate i.e. via openssl rand -base64 32
assert 'APP_SECRET' in os.environ, 'need to set APP_SECRET environ variable.'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET']
app.config['MONGO_URI'] = 'mongodb://localhost:27017/logindb'
mongo = PyMongo(app)
db = mongo.db

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # route or function where login occurs...

# create model
class User(UserMixin):
    
    #initialize use with email and name. Initialized _id and password_hash to NOne
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self._id = None
        self.password_hash = None
    
    # makes it so that you can access User.password as an attribute rather than 
    # by calling a getter method
    @property
    def password(self):
        raise AttributeError('password is write-only')
        
    # makes it so that you can call User.password = "" rather than calling a setter method    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    #verifies that the password passed in is equivalent to the user's password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # overload for flask_login
    def get_id(self):
        return str(self._id) # reuse MongoDB id
    
    # Given a key of name or email, searches db for User.
    # If not found, returns None.
    # If found, returns new User object with _id, name, email and password_hash from db. 
    def query(key):
        # pass in email or name as key
        doc = db.users.find_one({'$or' : [{'email' : key}, {'name' : key}]})
        if doc is None:
            return None
        u = User(email=doc['email'], name=doc['name'])
        u.password_hash=doc['password_hash']
        u._id = doc['_id']
        return u
    
    # Given a user _id, searches db for user.
    # If not found, returns None.
    # If found, returns new User object with _id, name, email and password_hash from db.
    def get(id):
        doc = db.users.find_one({'_id' : ObjectId(id)})
        if doc is None:
            return None
        u = User(email=doc['email'], name=doc['name'])
        u.password_hash=doc['password_hash']
        u._id = doc['_id']
        return u

    def tomongo(self):
        q = {'email' : self.email,
           'name' : self.name, 'password_hash' : self.password_hash}

        # If _id field is not None, then user must have been added to Mongo already, 
        # and update user's info.
        if self._id:
            db.users.update_one({'_id' : self._id}, {'$set' :q})
        else:
            # create new user

            # check a user under these keys does not exist yet!
            assert User.query(self.name) is None, 'user name {} already registered'.format(self.name)
            assert User.query(self.email) is None, 'email {} already registered'.format(self.email)
            # insert user's attributes into db, and retrieve _id given by Mongo as _id
            self._id = db.users.insert_one(q).inserted_id

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query(form.email_or_user.data)
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('internships'))
        flash('invalid username or password.')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # force logout
    logout_user()

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        name = form.username.data
        user = User(email=email, name=name)
        user.password = form.password.data # this calls the hash setter
        try:
            user.tomongo()
            login_user(user, form.remember_me.data)
            return redirect(url_for('internships'))
        except Exception as e:
            flash(str(e))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

# automatically redirect to internships page        
@app.route('/')
@login_required
def index():
    return redirect(url_for('internships'))

# edit this to be the internships page and return a template of the internships          
@app.route('/internships', methods=['GET', 'POST'])
@login_required
def internships():
    form = InternshipForm(method='POST')
    user_id = session.get('user_id')
    
    if form.submit.data and form.validate_on_submit():
        new_internship = dict(            
            user_id = ObjectId(user_id),
            company = form.company.data,
            medium = form.medium.data,
            position = form.position.data, 
            location = form.location.data, 
            notes = form.notes.data, 
            documents = form.documents.data,
            status = form.status.data
            )
        db.internships.insert_one(new_internship)
        
    internships = list(db.internships.find({'user_id' : ObjectId(user_id)}))
    print(internships)
    internships_obs = [Internship(**internship) for internship in internships]
    table = InternshipTable(internships_obs)
    
    return render_template('internships.html', form=form, table=table)

@app.route('/about')
@login_required
def about():
    pass



if __name__ == '__main__':
    app.run(debug=True)

