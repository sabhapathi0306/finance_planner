import re

#-----------account/users-------------------#
SELECT_USER_TABLE = 'select email,password,username from users where email = %s'
SELECT_USER_EMAIL = 'select email from users;'
USER_INFO_INSERT =  'INSERT INTO users(email, password, username, status, unique_value, date) values (%s, %s, %s, %s, %s, %s);'
ACCOUNT_INFO_INSERT = 'INSERT INTO account_details(email, unique_value) values (%s, %s);'
SELECT_ACCOUNT_INFO = 'select unique_value from account_details where unique_value = %s'
INSERT_GOALS = 'INSERT INTO goals (unique_value) values (%s);'
GET_DEATILS = """select name, total_income,
        budgeted_income, save, planned_type,month from  account_details
        where unique_value=%s;
        """
GET_STATUS = """SELECT u.status, u.password
FROM users u 
LEFT JOIN account_details a 
ON u.unique_value = a.unique_value 
WHERE u.unique_value = %s;"""

# ----------------wallet------------------------------------#
GOAL_SELECT_INFO = "SELECT goal_category FROM goals WHERE unique_value = %s"
INSERT_GOAL = "INSERT INTO goals (unique_value, goal_category, goal_description, percentage, amount,date) VALUES (%s, %s, %s, %s, %s,%s)"
UPDATE_GOAL = "UPDATE goals SET percentage=%s, amount=%s, goal_description=%s, date=%s WHERE unique_value=%s AND goal_category=%s"
SELECT_UNIQUE_VALUE = 'SELECT unique_value from goals where unique_value = %s'
SAVE_AMOUNT_INFO  = (
    """SELECT save from account_details
    where unique_value = %s"""
)
GET_ALL_CATEGORY = 'SELECT category,date from budget_log where unique_value = %s'
GET_STATMENT = """SELECT category, description, spent_amount, date, remaining, expenses from budget_log where unique_value = %s;"""
GET_Budgeted_INCOME = """SELECT budgeted_income FROM account_details WHERE unique_value = %s"""
GET_TOTAL_INCOME = """SELECT total_income FROM account_details WHERE unique_value = %s"""
UPDATE_BUDGET_LOG = "UPDATE budget_log SET remaining = %s, expenses = %s WHERE unique_value = %s AND category = %s AND date=%s"
INSERT_INTO_BUDGET_LOG = """INSERT INTO budget_log(unique_value, date, category, spent_amount, description, remaining, expenses) values (
                %s, %s, %s, %s, %s, %s, %s);"""
SAVE_AMOUNT_INFO = """select save,month from account_details where unique_value=%s"""

#--------------------------Goals--------------------------------#
GET_GOAL_DETAILS = """select id,goal_description, amount, date from goals where unique_value=%s;"""

#--------------------------credit card---------------------------#
GET_CREDIT_DETALS = """select credit_card,credited_amount,due_amount,paid_amount,month from credit_details
where unique_value = %s;"""


def contains_only_digits(string) -> bool:
    """
    function checks whether string 
    contain digint or not.
    """
    return bool(re.match(r'^\d+$', string))


def check_for_cap(string)-> bool:
    """
    function checks whether string 
    contain capital letter.
    """
    return bool(re.search(r'[A-Z]', string))


def check_for_small(string) -> bool:
    """
    function checks whether string 
    contain small letter.
    """
    return bool(re.search(r'[a-z]', string))


def check_numeric(string)-> bool:
    """
    function checks whether string 
    contain numeric.
    """
    return bool(re.search(r'[0-9]', string))


def check_for_special_char(string)-> bool:
    """
    function checks whether string 
    contain any special character.
    """
    pattern = r'[!@#$%^&*()_+\-=\[\]\{\};:\'\"<>,\.\?\/\\`\|]'
    if re.search(pattern, string):
        return bool(
            check_for_cap(string)
            and check_for_small(string)
            and check_numeric(string)
        )
    else:
        return False
        
        
def new_regime(income):
    """
    function return the 
    taxble amount and 
    slab percentage for
    given income under
    new regime.
    """
    income = income*12
    income = income - 50000
    if income <= 250000:
        return 0, '0'
    elif income <= 500000:
        return 0.05*income, '5%'
    elif income <= 750000:
        return 0.1*income, '10%'
    elif income <= 100000:
        return 0.15*income, '15%'
    elif income <= 1250000:
        return 0.2*income, '20%'
    elif income <= 1500000:
        return 0.25*income, '25%'
    else:
        return 0.3*income, '30%'
    
    
def old_regime(income):
    """
    function return the 
    taxble amount and 
    slab percentage for
    given income under 
    old regime.
    """
    income = income*12
    income = income - 50000
    if income <= 250000:
        return 0, '0'
    elif income <= 500000:
        return 0.05*income, '5%'
    elif income <= 1000000:
        return 0.2*income, '20%'
    else:
        return 0.3*income, '30%'
