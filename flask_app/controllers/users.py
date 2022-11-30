from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')

@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginRegister.html')


@app.route('/register', methods = ['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect(request.referrer)

    if User.get_user_by_email(request.form):
        flash('This email already exists, try another!', 'emailSignUp')
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    flash('You created the user succesfully! You can now use it to log in! ', 'signUpSuccessful')
    return redirect(request.referrer)


@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    if not User.get_user_by_email(request.form):
        flash('Please enter a correct email!', 'emailLogin')
        return redirect(request.referrer)

    user= User.get_user_by_email(request.form)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')
    

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    return render_template('dashboard.html', loggedUser= User.get_user_by_id(data), recipes= Recipe.getAllRecipes())