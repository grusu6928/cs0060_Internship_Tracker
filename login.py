import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_table import Table, Col, ButtonCol
from flask import render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_bootstrap import Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash

class LoginForm(FlaskForm):

    email_or_user = StringField('Email or username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', [Length(min=1, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

# the following classes are for flask-table 
class InternshipTable(Table):
    classes = ['table', 'table-hover']
    _id = Col('_id', show=False)
    remove = ButtonCol('','remove', url_kwargs=dict(_id='_id'), button_attrs={'class' : 'glyphicon glyphicon-trash'})
    edit = ButtonCol('','edit', url_kwargs=dict(_id='_id'), button_attrs={'class' : 'glyphicon glyphicon-pencil'})
    company = Col('Company')
    position = Col('Position')
    location = Col('Location')
    notes = Col('Notes')
    documents = Col('Documents')

# Get some objects
class Internship(object):
    def __init__(self, company, position=None, location=None, notes=None, documents=None):
        self.company = company
        self.position = position
        self.location = location
        self.notes = notes
        self.documents = documents
  
internships = []
user = None
docs = []

class InternshipForm(FlaskForm):
    company = StringField('Company', [DataRequired(), Length(min=1, max=60)])
    position = StringField('Position')
    location = StringField('Location')
    notes = StringField('Notes')
    documents = StringField('Documents')
    submit = SubmitField('Submit')

#Populate the table
internships_table = InternshipTable(internships)


# make sure app secret exists
# generate i.e. via openssl rand -base64 32
assert 'APP_SECRET' in os.environ, 'need to set APP_SECRET environ variable.'

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/logindb'
app.config['SECRET_KEY'] = os.environ['APP_SECRET']
mongo = PyMongo(app)
db = mongo.db


# create indices on email and name


Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # route or function where login occurs...

# create model
class User(UserMixin):

    def __init__(self, email, name):
        self.email = email
        self.name = name
        self._id = None
        self.password_hash = None

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # overload for flask_login
    def get_id(self):
        return str(self._id) # reuse MongoDB id

    def query(key):
        # pass in email or name as key
        doc = db.users.find_one({'$or' : [{'email' : key}, {'name' : key}]})
        if doc is None:
            return None
        u = User(email=doc['email'], name=doc['name'])
        u.password_hash=doc['password_hash']
        u._id = doc['_id']
        return u

    def get(id):
        doc = db.users.find_one({'_id' : ObjectId(id)})
        if doc is None:
            return None
        u = User(email=doc['email'], name=doc['name'])
        u.password_hash=doc['password_hash']
        u._id = doc['_id']
        return u

    def tomongo(self):
        # update info in mongodb
        q = {'email' : self.email,
           'name' : self.name, 'password_hash' : self.password_hash}

        # if _id field is there, then retrieved user
        if self._id:
            db.users.update_one({'_id' : self._id}, {'$set' :q})
        else:
            # create new user

            # check a user under these keys does not exist yet!
            assert User.query(self.name) is None, 'user name {} already registered'.format(self.name)
            assert User.query(self.email) is None, 'email {} already registered'.format(self.email)

            self._id = db.users.insert_one(q).inserted_id

# edit this to be the internships page and return a template of the internships          
@app.route('/')
@login_required
def index():
    return redirect(url_for('internships'))
            
            
# edit this to be the internships page and return a template of the internships          
@app.route('/internships', methods=['GET', 'POST'])
@login_required
def internships():
    form = InternshipForm(method='POST')
    editform = InternshipForm(method='POST')
    if form.validate_on_submit():
        new_internship = dict(company = form.company.data, 
             position = form.position.data, 
             location = form.location.data, 
             notes = form.notes.data, 
             documents = form.documents.data 
             )
        db.internships.insert_one(new_internship)
        form.position.data = ''
        form.company.data = ''
        form.location.data = ''
        form.notes.data = ''
        form.documents.data = '' 
    internships = list(db.internships.find())
    for internship in internships: 
        internship['_id'] = str(internship['_id'])
    table = InternshipTable(internships)
    return render_template('internships.html', form=form, table=table, editform = editform)

@app.route('/remove/<string:_id>', methods=['GET', 'POST'])
@login_required
def remove(_id):
    db.internships.remove({'_id' : ObjectId(_id)})
    return redirect(url_for('internships'))

@app.route('/edit/<string:_id>', methods=['GET', 'POST'])
@login_required
def edit(_id):
    query = db.internships.find_one({'_id' : ObjectId(_id)})
    editform = InternshipForm(method='POST')
    form = InternshipForm(method='POST')
    if editform.validate_on_submit():
        new_internship = dict(company = form.company.data, 
             position = editform.position.data, 
             location = editform.location.data, 
             notes = editform.notes.data, 
             documents = editform.documents.data 
             )
        db.internships.insert_one(new_internship)
        db.internships.remove({'_id' : ObjectId(_id)})
        editform.position.data = ''
        editform.company.data = ''
        editform.location.data = ''
        editform.notes.data = ''
        editform.documents.data = ''
        return redirect(url_for('internships'))
    editform.position.data = query['position']
    editform.company.data = query['company']
    editform.location.data = query['location']
    editform.notes.data = query['notes']
    editform.documents.data = query['documents']
    internships = list(db.internships.find())
    for internship in internships: 
        internship['_id'] = str(internship['_id'])
    table = InternshipTable(internships)
    return render_template('internships.html',form=form, editform=editform, table=table)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/about')
@login_required
def about():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():

    # force logout
    logout_user()

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data, name=form.username.data)
        user.password = form.password.data # this calls the hash setter
        try:
            user.tomongo()
            return redirect(url_for('internships'))
        except Exception as e:
            flash(str(e))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
