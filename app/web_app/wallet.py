import datetime
import json
import os
import psycopg2

import hashlib

from dotenv import load_dotenv, find_dotenv
from flask import request, jsonify
from app.web_app.common_utils import(
    SAVE_AMOUNT_INFO, SELECT_UNIQUE_VALUE,
    GOAL_SELEC_INFO, UPDATE_GOAL, INSERT_GOAL,
    GET_ALL_CATEGORY, GET_STATMENT, GET_TOTAL_INCOME,
    UPDATE_BUDGET_LOG, INSERT_INTO_BUDGET_LOG,
    GET_MONTH_WISE_SAVING
    
)


class Wallet:
    
    @staticmethod
    def __db_connection():
        load_dotenv(find_dotenv())
        url = os.environ.get("DATABASE_URL")
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        return conn, cursor
    
    def __init__(self):
        self.db_connection, self.db_cursor = Wallet.__db_connection()
        
    def __convert_to_unique(self, string):
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
    
    def goal_calculator(self, data):
        """Goal calculator"""
        try:
            data = json.loads(data)
            # COURSOR = CONN.cursor()
            email = data.get('email', None)
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(SAVE_AMOUNT_INFO, (__unique_value,))
            save_amount = float(self.db_cursor.fetchone()[0])
            self.db_cursor.execute(SELECT_UNIQUE_VALUE, (__unique_value,))
            __accounts = [val[0] for val in self.db_cursor.fetchall()]
            if __unique_value in __accounts:
                output_list = []
                empty_list = ['', None]
                self.db_cursor.execute(GOAL_SELEC_INFO, (__unique_value,))
                db_goals = [t[0] for t in self.db_cursor.fetchall()]
                percentages = data.get('percentages', None)
                if db_goals:
                    goals = data['goals']
                    for count, _ in enumerate(percentages):
                        goal_name = goals[count]
                        percentage = percentages[count]
                        if percentage in empty_list or percentage is None:
                            percentage = 0
                        if save_amount == 0:
                            return f"Your savings is {save_amount} check account section !!"
                        value = (float(percentage)/100) * save_amount
                        total_amount = value
                        if goal_name in db_goals:
                            self.db_cursor.execute(UPDATE_GOAL, (percentage, total_amount, email, goal_name))
                        else:
                            self.db_cursor.execute(INSERT_GOAL, (__unique_value, goal_name, percentage, total_amount))
                        self.db_connection.commit()
                        output = {
                            'goal_name': goal_name,
                            'percentage': percentage,
                            'total_amount': total_amount
                        }
                        output_list.append(output)
                else:
                    # if the record doesn't exist, insert a new record with the goal dat
                    if percentages is None:
                        return "Please Provide Percentage details also !!"
                    for count, _ in enumerate(percentages):
                        goal_name = goals[count]
                        percentage = percentages[count]
                        if percentage in empty_list or percentage is None:
                            percentage = 0
                        if save_amount == 0:
                            return f"Your savings is {save_amount} check account section !!"
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
                            self.db_cursor.execute(INSERT_GOAL, (__unique_value, goal_name, percentage, total_amount))
                            self.db_connection.commit()
                            output = {
                                'goal_name': goal_name,
                                'percentage': percentage,
                                'total_amount': total_amount
                            }
                        output_list.append(output)
            else:
                output_list = [{'Message': 'Account doest not exits check credintial!!'}]

            return True
        
        except Exception:
            self.db_connection.close()
            return False
        
    
    
    def add_expenses(self, data):
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
            self.db_cursor.execute(GET_TOTAL_INCOME, (__unique_value,))
            income = self.db_cursor.fetchone()[0]
            remaining = float(income) - float(amount_spent)
            round_remaining = round(remaining, 2)
            print(categories)
            if category in categories:
                self.db_cursor.execute(UPDATE_BUDGET_LOG,
                            (round_remaining, __unique_value, category))
                message = "CATEGORY UPDATED SUCCESFULLY !!"
            else:
                self.db_cursor.execute(INSERT_INTO_BUDGET_LOG, (
                    __unique_value, date, 
                    category,amount_spent,
                    description,round_remaining
                ))
                message = "CATEGORY ADDED SUCCESFULLY !!"
            self.db_connection.commit()
            return True
        
        except Exception:
            self.db_connection.close()
            return False

        
        
    