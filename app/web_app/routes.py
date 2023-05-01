import json
from flask import request, render_template, url_for, redirect,session
from app.web_app import app
from flask import flash
from app.web_app.details import Details
from app.web_app.user import User
from app.web_app.wallet import Wallet



app.secret_key = '0987654321fyndproject'



@app.route('/')
def home():
    # Define variables for the navigation bar
    try:
        details = Details()
        if session is not None and 'loggedin' in session:
            # message = f"Hi {session['username']}"
            return render_template('<h2>HELLO<h2>')
            username=session['username']
            message = f"Hi {username}!!"
            flash(message, 'success')
            email = session.get('email', None)
            get_data = details.get_details(email)
            get_data['email'] = email
            expenses = details.get_expenses(session['email'])
            if len(expenses)==0:
                expenses = list('None')
            details = {
                'account_details': get_data,
                'expenses': expenses
            }
            print(details)
            return render_template('index.html', logged_in=username,
                                username=username, details=details)

        # Render the home.html template and pass the variables to it
        return render_template('index.html')
    except Exception:
        raise



@app.route('/login', methods=['GET', 'POST'])
def login():
    run_app = User()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        data = json.dumps({'email': email, 'password': password})
        status, username = run_app.login(data)
        if status:
            session['loggedin'] = True
            session['email'] = email
            session['username'] = username
            message = f"Login is Successfull {username}. Please Update account details!"        
            return redirect('/')
        else:
            message = "Please pass correct credintials!!"
            return render_template('login.html', message=message)
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """Registration"""
    run_app = User()
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        data = json.dumps({'username': username, 'password': password, 'email': email})
        if run_app.register(data):
            message = "Registration is Successfull. Please Login!"
            return redirect('/login')
        else:
            message = "Something went wrong please try again !!"
            return redirect('/registration')
    
    else:
        message = ""
    return render_template('registration.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('username', None)
   # Redirect to login page
   message='logout successfully !!'
   return redirect('/')


@app.route('/account', methods=['GET', 'POST'])
def account():
    run_app = User()
    if 'loggedin' not in session:
        return redirect('login')
    if request.method == 'POST':
        form_data = dict(request.form.items())
        form_data['email'] = session['email']
        dump_data = json.dumps(form_data)
        if run_app.update_details(dump_data):
            message  = "Account updated successfully!!"
        else:
            message = 'Something went wrong try again !!'
        return redirect('/')
    return render_template('account.html')


@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    wallet_details = Wallet()
    if 'loggedin' not in session:
        return redirect('/login')
    if request.method != 'POST':
        return render_template('wallet.html')
    action = request.form['action']
    if action == 'update_budget':
        form_data = dict(request.form.items())
        form_data['email'] = session['email']
        data = json.dumps(form_data)
        if wallet_details.add_expenses(data):
            message = 'Expenses added successfully!!'
            return redirect('/')
        message = 'Something went wrong try again'
    elif action == 'update_goal':
        form_data = dict(request.form.items())
        form_data['email'] = session['email']
        # process the goal update here
        data = json.dumps(form_data)
        if wallet_details.goal_calculator(data):
            message = 'Goal added successfully!!'
            return redirect('/')
        message = 'Something went wrong try again'
    return render_template('wallet.html', message=message)


@app.route('/learning')
def learning():
    return render_template('learning.html')

