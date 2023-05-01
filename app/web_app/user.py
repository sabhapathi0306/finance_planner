import datetime
import json
import os
import re
import hashlib
import psycopg2



from app.web_app.common_utils import (
    SELECT_USER_TABLE, check_for_special_char,SELECT_USER_EMAIL,
    USER_INFO_INSERT, ACCOUNT_INFO_INSERT,contains_only_digits,
    SELECT_ACCOUNT_INFO, INSERT_GOALS, GET_DEATILS, GET_STATUS,
    old_regime, new_regime
)
from dotenv import load_dotenv,find_dotenv

class User:

    @staticmethod
    def __db_connection():
        load_dotenv(find_dotenv())
        url = os.environ.get("DATABASE_URL")
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        return conn, cursor
    
    def __init__(self):
        self.db_connection, self.db_cursor = User.__db_connection()
        
    def __convert_to_unique(self, string):
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
        

    def login(self, data):
        """login"""
        # data = request.get_json()
        try:
            data = json.loads(data)
            email = data.get('email', None)
            password = data.get('password', None)
            if email is None or password is None:
                return 'EMAIL AND PASSWORD REQUIRED!!'
            # self.db_cursor = CONN.self.db_cursor()
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
        except Exception:
            self.db_connection.close()
            return False
        
   
    
    def register(self, data):
        """Registration"""
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
            # self.db_cursor = CONN.self.db_cursor()
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
                self.db_cursor.execute(ACCOUNT_INFO_INSERT, (email, unique_value))
                self.db_connection.commit()
                return 'SUCCESSFULLY REGISTERED!!'

        else:
            return '''PLEASE PROVIDE PASSWORD LIKE THIS
                password length should be >= 8 and must one capital,
                small, numerical and special character.
                Example: Ramnath!234
                ''' 

    def update_details(self, data):
        """account"""
        try:
            data = json.loads(data)
            print(data)
            query_value = []
            columns = []
            # self.db_cursor = CONN.self.db_cursor()
            __unique_value  = self.__convert_to_unique(data.get('email', None))
            self.db_cursor.execute(SELECT_ACCOUNT_INFO, (__unique_value,))
            __accounts = [val[0] for val in self.db_cursor.fetchall()]
            if __unique_value in __accounts:
                self.db_cursor.execute(INSERT_GOALS, (__unique_value,))
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
                if 'month' not in data:
                    month = datetime.datetime.now().strftime('%Y-%m')
                else:
                    month = data['month']
                query_value.append(month)
                columns.append('month')
                if 'totalincome' in data:
                    income = data['totalincome']
                    tax_details_new, new_type = new_regime(float(income))
                    tax_details_old, old_type = old_regime(float(income))
                    income = float(income) - tax_details_new
                    query_value.append(income)
                    query_value.append(tax_details_new)
                    query_value.append(tax_details_old)
                    columns.append('total_income')
                    columns.append('new_tax')
                    columns.append('old_tax')
                if 'needs' in data and contains_only_digits(data['needs']):
                    needs_value = float(data['needs'])/100
                    needs_amount = needs_value*float(income)
                    columns.append('needs')
                    query_value.append(needs_amount)
                    planning += data['needs']+ "+"
                else:
                    message = "needs not proper passed"

                if 'wants' in data and contains_only_digits(data['wants']):
                    wants_value = float(data['wants'])/100
                    wants_amount = wants_value*float(income)
                    columns.append('wants')
                    query_value.append(wants_amount)
                    planning += data['wants'] + "+"
                else:
                    message = "wants not proper passed"

                if 'save' in data and contains_only_digits(data['save']):
                    save_value = float(data['save'])/100
                    save_amount = save_value*float(income)
                    columns.append('save')
                    query_value.append(save_amount)
                    planning += data['save']
                else:
                    message = "save_or_goals not proper passed"
                
                __fixes_point = 1
                __check_plan_point = needs_value+wants_value+save_value
                if __check_plan_point > __fixes_point:
                    message = f"""
                    Provided plane [{__check_plan_point}] is greater than 100 % 
                    So keeping Default value for user accout 
                    and you can coustomize it anytime!!
                    """
                    planning = "50"+"30"+"20"
                    needs_amount = 0.5 * float(data['totalincome'])
                    wants_amount = 0.3 * float(data['totalincome'])
                    save_amount = 0.2 *  float(data['totalincome'])
                query_value.append(planning)
                columns.append('planned_type')
                budgeted_incomed = needs_amount+wants_amount
                # remaining=float(income)-budgeted_incomed
                query_value.append(budgeted_incomed)
                columns.append('budgeted_income')
                if len(columns) != len(query_value):
                    return False
                query_value.append(__unique_value)
                tup = tuple(query_value)
                UPDATE_ACCOUNT = f"""UPDATE account_details SET
                {','.join([f'{col}= %s' for col in columns])} WHERE unique_value = %s"""
                self.db_cursor.execute(UPDATE_ACCOUNT, tup)
                self.db_connection.commit()
                return True
            else:
                print('Nope')
                return False
        
        except Exception as exp_err:
            self.db_connection.close()
            return "SOMETHING WENT WRONG !!"
        

if __name__ == '__main__':
    print('IMPORTED')