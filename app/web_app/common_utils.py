import re

import psycopg2



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
GOAL_SELEC_INFO = "SELECT goal_name FROM goals WHERE unique_value = %s"
INSERT_GOAL = "INSERT INTO goals (unique_value, goal_name, percentage, total_amount) VALUES (%s, %s, %s, %s)"
UPDATE_GOAL = "UPDATE goals SET percentage=%s, total_amount=%s WHERE unique_value=%s AND goal_name=%s"
SELECT_UNIQUE_VALUE = 'SELECT unique_value from goals where unique_value = %s'
SAVE_AMOUNT_INFO  = (
    """SELECT save from account_details
    where unique_value = %s"""
)
GET_ALL_CATEGORY = 'SELECT category from budget_log where unique_value = %s'
GET_STATMENT = """SELECT category, description, spent_amount, date, remaining from budget_log where unique_value = %s;"""
GET_TOTAL_INCOME = """SELECT total_income FROM account_details WHERE unique_value = %s"""
UPDATE_BUDGET_LOG = "UPDATE budget_log SET remaining = %s WHERE unique_value = %s AND category = %s"
INSERT_INTO_BUDGET_LOG = """INSERT INTO budget_log(unique_value, date, category, spent_amount, description, remaining) values (
                %s, %s, %s, %s, %s, %s);"""
GET_MONTH_WISE_SAVING = """SELECT save, month from account_details where email = %s"""
# ADMIN_TABLE  = """
# create table admin(
#     name varchar,
#     email varchar,
#     password varchar,
#     date DATE,
#     unique_value varchar,
#     CONSTRAINT unique_admin_value UNIQUE(unique_value)
# )
# """

# SELECT_ADMIN = """
# select email, password from admin where unique_value = %s;
# """
# USER_TABLE = """
# create table users(
#     username varchar,
#     email varchar,
#     password varchar,
#     date DATE,
#     unique_value varchar,
#     status varchar,
#     CONSTRAINT unique_user_value UNIQUE(unique_value)
# )with (fillfactor=90);
# """

# ACCOUNT_DETAILS = """
# create table account_details(
#     id SERIAL PRIMARY KEY,
#     unique_value varchar,
#     email varchar,
#     name varchar,
#     total_income varchar,
#     needs varchar,
#     wants varchar,
#     save varchar,
#     budgeted_income varchar,
#     month varchar,
#     CONSTRAINT fk_account_unique_value
#         FOREIGN KEY (unique_value) 
#         REFERENCES users (unique_value)
# )with (fillfactor=90);
# """

# BUDGET_LOG = """
# CREATE TABLE budget_log (
#   id SERIAL PRIMARY KEY,
#   unique_value VARCHAR,
#   category VARCHAR,
#   description VARCHAR,
#   spent_amount VARCHAR,
#   remaining VARCHAR,
#   date DATE,
#   CONSTRAINT fk_account_unique_value
#     FOREIGN KEY (unique_value) 
#     REFERENCES users (unique_value)
# )with (fillfactor=90);
# """

# GOALS = """
# create table goals(
#     id SERIAL PRIMARY KEY,
#     unique_value varchar,
#     goal_name varchar,
#     status varchar,
#     date DATE,
#     CONSTRAINT fk_account_unique_value
#     FOREIGN KEY (unique_value) 
#     REFERENCES users (unique_value)
# )with (fillfactor=90);
# """

# SUBSCRIPTION = """
# create table subscriptions(
#     id SERIAL PRIMARY KEY,
#     unique_value varchar,
#     name varchar,
#     amount varchar,
#     renew DATE,
#     month DATE,
#     CONSTRAINT fk_account_unique_value
#     FOREIGN KEY (unique_value) 
#     REFERENCES users (unique_value)
# )with (fillfactor=90);
# """
# CREDIT_DETAILS = """create table credit_details(
#     id SERIAL PRIMARY KEY,
#     unique_value varchar,
#     credit_card  varchar,
#     credited_amount varchar,
#     due_amount varchar,
#     paid_amount varchar,
#     month varchar,
#     CONSTRAINT fk_account_unique_value
#     FOREIGN KEY (unique_value) 
#     REFERENCES users (unique_value)
# )with (fillfactor=90);
# """

# import os
# import psycopg2
# from dotenv import load_dotenv
# # url = 'postgres://bvqlhmje:US493uZiLwKwPyc_a_V_er4wwCFSu1iI@lallah.db.elephantsql.com/bvqlhmje'
# # # print(url)
# load_dotenv()
# url = os.environ.get("DATABASE_URL")
# conn = psycopg2.connect(url)

# cursor = conn.cursor()
# cursor.execute(USER_TABLE)
# cursor.execute(ACCOUNT_DETAILS)
# cursor.execute(BUDGET_LOG)
# cursor.execute(GOALS)
# cursor.execute(SUBSCRIPTION)
# cursor.execute(CREDIT_DETAILS)
# conn.commit()
# cursor.execute("TRUNCATE TABLE users CASCADE;")
# cursor.execute("TRUNCATE TABLE goals CASCADE;")
# # cursor.execute('TRUNCATE TABLE budget_log;')
# conn.commit()

# # cursor.execute(GOALS)
# # cursor.execute(SUBSCRIPTION)
# # conn.close()

# # print('DONE')

# cursor.execute("""SELECT table_name FROM information_schema.tables
#        WHERE table_schema = 'public'""")
# for table in cursor.fetchall():
#     print(table)
    
def contains_only_digits(string):
    return bool(re.match(r'^\d+$', string))

def check_for_cap(string):
    return bool(re.search(r'[A-Z]', string))

def check_for_small(string):
    return bool(re.search(r'[a-z]', string))

def check_numeric(string):
    return bool(re.search(r'[0-9]', string))

def check_for_special_char(string):
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
    if income <= 250000:
        return 0, 'NEW REGIME'
    elif income>250000 and income<=500000:
        return 0.05*income, 'NEW REGIME'
    elif income>500000 and income<=750000:
        return 0.1*income+12500, 'NEW REGIME'
    elif income>750000 and income<=100000:
        return 0.15*income+37500, 'NEW REGIME'
    elif income>100000 and income<=1250000:
        return 0.2*income+75000, 'NEW REGIME'
    elif income>1250000 and income<=1500000:
        return 0.25*income+125000, 'NEW REGIME'
    else:
        return 0.3*income+187500, 'NEW REGIME'
    
def old_regime(income):
    if income <= 250000:
        return 0, 'OLD REGIME'
    elif income>250000 and income<=500000:
        return 0.05*income, 'OLD REGIME'
    elif income>500000 and income<=1000000:
        return 0.2*income+12500, 'OLD REGIME'
    else:
        return 0.3*income+112500, 'OLD REGIME'
