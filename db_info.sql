
 USER_TABLE = """
 create table users(
     username varchar,
     email varchar,
     password varchar,
     date DATE,
     unique_value varchar,
     status varchar,
     CONSTRAINT unique_user_value UNIQUE(unique_value)
 )with (fillfactor=90);
 """

 ACCOUNT_DETAILS = """
 create table account_details(
     id SERIAL PRIMARY KEY,
     unique_value varchar,
     email varchar,
     name varchar,
     total_income varchar,
     needs varchar,
     wants varchar,
     save varchar,
     planned_type varchar,
     budgeted_income varchar,
     new_tax varchar,
     old_tax varchar,
     month varchar,
     CONSTRAINT unique_account_value UNIQUE(unique_value)
 )with (fillfactor=90);
 """

 BUDGET_LOG = """
 CREATE TABLE budget_log (
   id SERIAL PRIMARY KEY,
   unique_value VARCHAR,
   category VARCHAR,
   description VARCHAR,
   spent_amount VARCHAR,
   remaining VARCHAR,
   date DATE,
   CONSTRAINT fk_account_unique_value
     FOREIGN KEY (unique_value) 
     REFERENCES users (unique_value)
 )with (fillfactor=90);
 """

 GOALS = """
 create table goals(
     id SERIAL PRIMARY KEY,
     unique_value varchar,
     goal_category varchar,
     goal_description varchar,
     date DATE,
     amount varchar,
     percentage varchar,
     CONSTRAINT fk_account_unique_value
     FOREIGN KEY (unique_value) 
     REFERENCES users (unique_value)
 )with (fillfactor=90);
 """

 SUBSCRIPTION = """
 create table subscriptions(
     id SERIAL PRIMARY KEY,
     unique_value varchar,
     name varchar,
     amount varchar,
     renew DATE,
     month DATE,
     CONSTRAINT fk_account_unique_value
     FOREIGN KEY (unique_value) 
     REFERENCES users (unique_value)
 )with (fillfactor=90);
 """
 CREDIT_DETAILS = """create table credit_details(
     id SERIAL PRIMARY KEY,
     unique_value varchar,
     credit_card  varchar,
     credited_amount varchar,
     due_amount varchar,
     paid_amount varchar,
     month varchar,
     CONSTRAINT fk_account_unique_value
     FOREIGN KEY (unique_value) 
     REFERENCES users (unique_value)
 )with (fillfactor=90);
 """