from flask import Flask,request,render_template, redirect, session, flash
from models import Feedback, db, connect_db,pg_user, pg_pwd, User
from forms import RegisterForm, LoginForm, FeedBackForm
from flask_bcrypt import Bcrypt
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@localhost:5432/twitter_db".format(username=pg_user, password=pg_pwd)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'welcomehomesir'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=True


connect_db(app)
db.create_all()


pg_user = "tester"
pg_pwd = "testing123"


def connect_db(app):
    db.app = app
    db.init_app(app) 

bcrypt = Bcrypt()

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/secret')
def secret():
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        return redirect('/login')
    return render_template('secret.html')

@app.route('/users/<username>')
def user_deatils(username):
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        return redirect('/login')
    user = User.query.get(username)
    return render_template('user_details.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username,password,email,first_name,last_name)
        return redirect('/secret')
    return render_template('register_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.authenticate(username, password):
            session['user_id'] = username
            return redirect(F'/users/{username}')
    return render_template('login_form.html', form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'user_id' not in session:
        flash('You must be logged in to do this')
        return redirect('/login')
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    form = FeedBackForm()
    if 'user_id' not in session:
        flash('You must be logged in to do this')
        return redirect('/login')
    if form.validate_on_submit():
        content = form.content.data
        title = form.title.data
        new_feedback = Feedback(title=title,content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback_form.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    form = FeedBackForm()
    if 'user_id' not in session:
        flash('You must be logged in to do this')
        return redirect('/login')
    if form.validate_on_submit():
        feedback = Feedback.query.get(feedback_id)
        feedback.content = form.content.data
        feedback.title = form.title.data
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    feedback = Feedback.query.get(feedback_id)
    form.title.data = feedback.title
    form.content.data = feedback.content

    return render_template('feedback_form.html', form=form, id=feedback.id)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if session['user_id'] != feedback.username:
        flash('You can not do this')
        return redirect('/login')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')