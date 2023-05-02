import datetime
import json
import os
import psycopg2

import hashlib

from dotenv import load_dotenv, find_dotenv
from app.web_app.common_utils import(
    SAVE_AMOUNT_INFO, SELECT_UNIQUE_VALUE,
    GOAL_SELECT_INFO, UPDATE_GOAL, INSERT_GOAL,
    GET_ALL_CATEGORY, GET_Budgeted_INCOME,
    UPDATE_BUDGET_LOG, INSERT_INTO_BUDGET_LOG,
)
from app.web_app.utils import loggers

LOGGER = loggers.setup_logger('finance_planner', 'wallet.log')


class Wallet:
    """
    class contain methods
    to perform budget updations,
    goals updation, credit card
    details updations and also
    insert or update the data 
    into database.
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
        self.db_connection, self.db_cursor = Wallet.__db_connection()
        
        
    def __convert_to_unique(self, string):
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
    
    
    def goal_calculator(self, data):
        """Goal calculator"""
        try:
            data = json.loads(data)
            email = data.get('email', None)
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(SAVE_AMOUNT_INFO, (__unique_value,))
            save_amount = float(self.db_cursor.fetchone()[0])
            self.db_cursor.execute(SELECT_UNIQUE_VALUE, (__unique_value,))
            __accounts = [val[0] for val in self.db_cursor.fetchall()]
            goal_category = data.get('goal_category')
            description = data.get('description')
            percentage = data.get('percentage', 0)
            if __unique_value in __accounts:
                output_list = []
                self.db_cursor.execute(GOAL_SELECT_INFO, (__unique_value,))
                db_goals = [t[0] for t in self.db_cursor.fetchall()]
                percentages = data.get('percentage', None)
                date = data['date']
                if date is None:
                    date = datetime.datetime.now().strftime('%Y-%m-%d')
                if db_goals:
                    goal_category = data['goal_category']
                    empty_list = ['', None]
                    if percentage in empty_list or percentage is None:
                        percentage = 0
                    value = (float(percentage)/100) * save_amount
                    total_amount = value
                    if goal_category in db_goals:
                        self.db_cursor.execute(UPDATE_GOAL, (percentage, total_amount,description, date, __unique_value, goal_category))
                    else:
                         self.db_cursor.execute(INSERT_GOAL, (__unique_value, goal_category, description, percentage, total_amount, date))
                    self.db_connection.commit()

                else:
                    value = (float(percentages)/100) * save_amount
                    if data.get('check') == 'y':
                        months = int(data['year']) * 12
                        expected = value * months
                        output = {
                            'expected': expected,
                            'year': data['year'],
                            'months': months
                        }
                    else:
                        total_amount = value
                        self.db_cursor.execute(INSERT_GOAL, (__unique_value, goal_category, description, percentage, total_amount, date))
                        self.db_connection.commit()

            else:
                output_list = [{'Message': 'Account doest not exits check credintial!!'}]

            return True

        except Exception as exp_err:
            LOGGER.error(exp_err)
            return False
        

    def add_expenses(self, data):
        """expenses updations"""
        try:
            data = json.loads(data)
            # COURSOR = CONN.cursor()
            date = data.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
            email = data.get('email', None)
            category = data.get('category', None)
            amount_spent = data.get('spentamount', None)
            description = data.get('description', None)
            if amount_spent is None:
                return "Please Enter the spent amount"
            description = data.get('description', None)
            if email is None:
                return "Something Wrong!!"
            __unique_value = self.__convert_to_unique(email)
            self.db_cursor.execute(GET_ALL_CATEGORY, (__unique_value, ))
            categories = [val[0] for val in self.db_cursor.fetchall()]
            dates = [val[1] for val in self.db_cursor.fetchall()]
            self.db_cursor.execute(GET_Budgeted_INCOME, (__unique_value,))
            income = self.db_cursor.fetchone()[0]
            remaining = float(income) - float(amount_spent)
            expenses = float(amount_spent)
            round_remaining = round(remaining, 2)
            if category in categories and date in dates:
                self.db_cursor.execute(UPDATE_BUDGET_LOG,
                            (round_remaining, __unique_value, category, expenses, date))
                message = "CATEGORY UPDATED SUCCESFULLY !!"
            else:
                self.db_cursor.execute(INSERT_INTO_BUDGET_LOG, (
                    __unique_value, date, 
                    category,amount_spent,
                    description,round_remaining, expenses
                ))
                message = "CATEGORY ADDED SUCCESFULLY !!"
            self.db_connection.commit()
            return True
        
        except Exception as exp_err:
            LOGGER.error(exp_err)
            return False

        
    def credit_card_details(self, data):
        """credit card details updation"""
        try:
            data = json.loads(data)
            columns = []
            query_value = []
            email = data.get('email', None)
            credit_card = data.get('credit_card', None)
            query_value.append(credit_card)
            columns.append('credit_card')
            credited_amount = data.get('credited_amount', None)
            query_value.append(credited_amount)
            columns.append('credited_amount')
            due_amount = data.get('due_amount', None)
            query_value.append(due_amount)
            columns.append('due_amount')
            paid_amount = data.get('paid_amount', None)
            query_value.append(paid_amount)
            columns.append('paid_amount')
            month = data.get('month', None)
            query_value.append(month)
            columns.append('month')
            if email is None:
                return "Something Wrong!!"
            __unique_value = self.__convert_to_unique(email)
            query_value.append(__unique_value)
            columns.append('unique_value')
            tup = tuple(query_value)
            INSERT_ACCOUNT = f"""INSERT INTO credit_details(
                {','.join([f'{col}' for col in columns])}) values (
                {','.join([f"'{col}'" for col in tup])});"""
            self.db_cursor.execute(INSERT_ACCOUNT)
            self.db_connection.commit()
            return True
        
        except Exception as exp_err:
            LOGGER.error(exp_err)
            return False
        
    