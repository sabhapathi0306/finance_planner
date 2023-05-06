import os
import datetime
import json
import hashlib
import psycopg2

from app.web_app.common_utils import (
    SELECT_USER_TABLE, SELECT_USER_EMAIL,
    check_for_special_char,
    USER_INFO_INSERT, contains_only_digits,
    new_regime, old_regime,
    GET_MONTH_DETAILS
)
from dotenv import load_dotenv,find_dotenv
from app.web_app.utils import loggers

LOGGER = loggers.setup_logger('finance_planner', 'user.log')


class User:
    """
    class contain methods to 
    perform registration, login
    account updation operation
    and also update all data into
    database.
    """
    @staticmethod
    def __db_connection():
        try:
            load_dotenv(find_dotenv())
            url = os.environ.get("DATABASE_URL")
            conn = psycopg2.connect(url)
            cursor = conn.cursor()
            return conn, cursor
        
        except Exception as exp_err:
            LOGGER.error(exp_err)
            
    
    def __init__(self):
        self.db_connection, self.db_cursor = User.__db_connection()
        
        
    def __convert_to_unique(self, string):
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
        

    def login(self, data):
        """login"""
        try:
            data = json.loads(data)
            email = data.get('email', None)
            password = data.get('password', None)
            if email is None or password is None:
                return 'EMAIL AND PASSWORD REQUIRED!!'
            self.db_cursor.execute(SELECT_USER_TABLE, (email,))
            tup_val = self.db_cursor.fetchall()
            db_email = [val[0] for val in tup_val]
            db_password = [val[1] for val in tup_val]
            db_username = [val[2] for val in tup_val]
            self.db_connection.commit()
            return (
                True, ''.join(db_username)
                if email in db_email and password in db_password
                else False
            )
        except Exception as exp_err:
            LOGGER.error(exp_err)
            return False
        
    
    def register(self, data):
        """Registration"""
        try:
            data = json.loads(data)
            username = data.get('username', None)
            email = data.get('email', None)
            password = data.get('password', None)
            if username is None or email is None:
                return 'ALL FEILDS ARE REQUIRED !!'
            password_len = len(password)
            if password_len < 8:
                return '''PLEASE PROVIDE PASSWORD LIKE THIS
                    password length should be >= 8 and must one capital,
                    small, numerical and special character.
                    Example: Ramnath!234
                    '''
            if check_for_special_char(password):
                self.db_cursor.execute(SELECT_USER_EMAIL)
                emails_tup = self.db_cursor.fetchall()
                emails = [val[0] for val in emails_tup]
                if email in emails:
                    self.db_cursor.close()
                    return 'EMAIL ALREADY USED!!'
                else:
                    unique_value = self.__convert_to_unique(email)
                    status = 'ACTIVE'
                    Date = datetime.datetime.now()
                    self.db_cursor.execute(USER_INFO_INSERT, (email, password, username, status, unique_value, Date))
                    # self.db_cursor.execute(ACCOUNT_INFO_INSERT, (email, unique_value))
                    self.db_connection.commit()
                    return 'SUCCESSFULLY REGISTERED!!'

            else:
                return '''PLEASE PROVIDE PASSWORD LIKE THIS
                    password length should be >= 8 and must one capital,
                    small, numerical and special character.
                    Example: Ramnath!234
                    ''' 
        except Exception as exp_err:
            LOGGER.error(exp_err)


    def update_details(self, data):
        """account details updation"""
        try:
            data = json.loads(data)
            query_value = []
            columns = []
            __unique_value  = self.__convert_to_unique(data.get('email', None))
            income = 0
            planning = ''
            needs_value = 0
            wants_value = 0
            save_value = 0
            needs_amount = 0
            wants_amount = 0
            save_amount = 0
            if 'name' in data:
                query_value.append(data['name'])
                columns.append('name')
            if 'totalincome' in data:
                total_income = data['totalincome']
                tax_details_new,_ = new_regime(float(total_income))
                tax_details_old,_ = old_regime(float(total_income))
                income = float(total_income) - (tax_details_new/12)
                query_value.extend((total_income, tax_details_new, tax_details_old))
                columns.append('total_income')
                columns.append('new_tax')
                columns.append('old_tax')
            if 'needs' in data and contains_only_digits(data['needs']):
                needs_value = float(data['needs'])/100
                needs_amount = needs_value*float(income)
                columns.append('needs')
                query_value.append(needs_amount)
                planning += data['needs']+ "+"
            if 'wants' in data and contains_only_digits(data['wants']):
                wants_value = float(data['wants'])/100
                wants_amount = wants_value*float(income)
                columns.append('wants')
                query_value.append(wants_amount)
                planning += data['wants'] + "+"
            if 'save' in data and contains_only_digits(data['save']):
                save_value = float(data['save'])/100
                save_amount = round(save_value*float(income),2)
                columns.append('save')
                query_value.append(save_amount)
                planning += data['save']
            __fixes_point = 1
            __check_plan_point = needs_value+wants_value+save_value
            if __check_plan_point > __fixes_point:
                planning = "50"+"30"+"20"
                needs_amount = 0.5 * float(data['totalincome'])
                wants_amount = 0.3 * float(data['totalincome'])
                save_amount = 0.2 *  float(data['totalincome'])
            query_value.append(planning)
            columns.append('planned_type')
            budgeted_incomed = round(needs_amount+wants_amount,2)
            query_value.append(budgeted_incomed)
            columns.append('budgeted_income')
            if len(columns) != len(query_value):
                return False
            self.db_cursor.execute(GET_MONTH_DETAILS, (__unique_value,))
            month_value = self.db_cursor.fetchall()
            month_list = [val[0] for val in month_value]
            unique_list = [val[1] for val in month_value]
            month = data.get('month')
            if month in month_list and __unique_value in unique_list:
                query_value.append(month)
                query_value.append(__unique_value)
                tup = tuple(query_value)
                UPDATE_ACCOUNT = f"""UPDATE account_details SET
                {','.join([f'{col}= %s' for col in columns])}
                WHERE month = %s and unique_value=%s"""
                self.db_cursor.execute(UPDATE_ACCOUNT, tup)
                self.db_connection.commit()
            else:
                query_value.append(month)
                columns.append('month')
                query_value.append(__unique_value)
                columns.append('unique_value')
                query_value.append(data['email'])
                columns.append('email')
                tup = tuple(query_value)
                INSERT_ACCOUNT = f"""INSERT INTO account_details(
                {','.join([f'{col}' for col in columns])}) values (
                {','.join([f"'{col}'" for col in tup])});"""
                self.db_cursor.execute(INSERT_ACCOUNT)
                self.db_connection.commit()
            return True

        except Exception as exp_err:
            LOGGER.error(exp_err)
            return False
        

if __name__ == '__main__':
    print('IMPORTED')
