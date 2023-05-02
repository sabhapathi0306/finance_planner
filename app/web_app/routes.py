import json
from flask import request, render_template, url_for, redirect,session
from app.web_app import app
from flask import flash
from app.web_app.details import Details
from app.web_app.user import User
from app.web_app.wallet import Wallet



app.secret_key = '0987654321fyndproject'

information = Details()


@app.route('/')
def home():
    """
    function retrive all data from the
    database and reflect it on front end
    side.
    Information is obj refrence for Details
    class which is imported from details.py
    """
    try:
        if 'loggedin' in session and session['loggedin']:
            username=session['username']
            email = session.get('email', None)
            get_data, status = information.get_details(email)
            if not status:
                render_template('index.html')
            get_data['email'] = session['email']
            expenses = information.get_expenses(session['email'])
            tax_details = information.get_tax_details(session['email'])
            goal_details = information.get_goals(session['email'])
            get_credit_details = information.get_credit_details(session['email'])
            save_details = information.save_amount_details(session['email'])
            if len(expenses)==0:
                expenses = list('None')
            details = {
                'account_details': get_data,
                'expenses': expenses,
                'tax_details':tax_details,
                'goal_details':goal_details,
                'credit_details':get_credit_details,
                'save_details': save_details
            }
            return render_template('index.html', logged_in=username,
                                username=username, details=details)
        else:
            return render_template('index.html')
        
    except Exception:
        message = 'Something went wrong please try again !!'
        return render_template('index.html' , message=message)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    function process the login
    details which is posted
    from front end.
    """
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
    """
    function process the registration
    details passed through forms.
    
    here form data are dumped before passing
    into register function
    
    run_app is the obj reference for User
    class.
    """
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
    """ 
    function operates the logout
    logic and clears all the 
    session information.
    """
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    # Redirect to login page
    message='logout successfully !!'
    return redirect('/')


@app.route('/account', methods=['GET', 'POST'])
def account():
    """
    function collects the account details and
    passed into update_details to perform the 
    account updations.
    """
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
    """
    function collects all expenses,
    goals and credit card data passed
    and only perform based on if condition
    logic.
    i.e if only expenses details passed
    only perform follow statement.
    """
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
    elif action == 'update_credit':
        form_data = dict(request.form.items())
        form_data['email'] = session['email']
        data = json.dumps(form_data)
        if wallet_details.credit_card_details(data):
            return redirect('/')

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
    """
    render the learning
    page
    """
    return render_template('learning.html')


@app.route('/investment')
def investment():
    """
    render the investment
    page
    """
    return render_template('investment.html')