import os
import hashlib
import psycopg2
from app.web_app.common_utils import (
    GET_DEATILS, GET_STATUS,
    GET_STATMENT, GET_TOTAL_INCOME, 
    SAVE_AMOUNT_INFO,GET_GOAL_DETAILS,
    GET_CREDIT_DETALS
)
from dotenv import load_dotenv,find_dotenv
from app.web_app.common_utils import (
    new_regime, old_regime
)
from app.web_app.utils import loggers

LOGGER = loggers.setup_logger('finance_planner', 'user.log')


class Details:
    """
    class contains methods to 
    get the details/retrive data from
    database
    """
    @staticmethod
    def __db_connection():
        """
        static method which helps in creating conn
        with database
        """
        try:
            load_dotenv(find_dotenv())
            url = os.environ.get("DATABASE_URL")
            conn = psycopg2.connect(url)
            cursor = conn.cursor()
            return conn, cursor
        
        except Exception as exp_err:
            LOGGER.error(exp_err)
    
    
    def __init__(self):
        self.db_connection, self.db_cursor = Details.__db_connection()
        

    def __convert_to_unique(self, string):
        """
        method convert the email into unique
        values here hexdigest method used for
        unique value generation.
        """
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
    
    
    def get_details(self, email):
        """
        method return the wallet information
        from the database.
        """
        try:
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(GET_DEATILS, (__unique_value,))
            val_tup = self.db_cursor.fetchone()
            coum_tup = ('name', 'total_income', 'budgeted_income', 'save', 'planned_type', 'month')
            if val_tup is not None:
                details_dict = {coum_tup[i]: val_tup[i] for i in range(len(val_tup))}
                self.db_cursor.execute(GET_STATUS, (__unique_value, ))
                status_val_tup = self.db_cursor.fetchone()
                status_dict_tup= ('status', 'password')
                details_dict.update(status_dict)
                return details_dict, True
        except Exception:
            return {},False
        
    def get_expenses(self, email):
        """
        method return the details of
        expenses
        """
        try:
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(GET_STATMENT, (__unique_value,))
            val_tup = self.db_cursor.fetchall()
            coum_tup = ('category', 'description', 'spent_amount', 'date', 'remaining', 'expenses')
            lis  =[]
            for val in val_tup:
                deatils_dic = {
                    coum_tup[0]: val[0],
                    coum_tup[1]: val[1],
                    coum_tup[2]: val[2],
                    coum_tup[3]: val[3].strftime('%Y-%m-%d'),
                    coum_tup[4]: val[4],
                    coum_tup[5]:val[5]
                }
                lis.append(deatils_dic)
                
            return lis
        
        except Exception as exp_err:
            loggers.setup_logger.error(exp_err)
            return []
    
    
    def get_tax_details(self, email):
        """
        method return the tax details
        for provided the income
        """
        try:
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(GET_TOTAL_INCOME, (__unique_value,))
            val_tup = self.db_cursor.fetchone()[0]
            if val_tup is None:
                val_tup = 0
            result   = float(val_tup)
            new_regime_ans, new_percentage= new_regime(result)
            old_regime_ans, old_percentage= old_regime(result)
            return {
                'old_total': old_regime_ans,
                'old_percentage': new_percentage,
                'new_total': new_regime_ans,
                'new_percentage': old_percentage,
                'tax_after_amount_new': result - new_regime_ans,
                'tax_after_amount_old': result - old_regime_ans,
            }
        except Exception as exp_err:
            LOGGER.error(exp_err)
            return {}
    
    
    def get_goals(self, email):
        """
        method return goal details
        """
        __unique_value  = self.__convert_to_unique(email)
        self.db_cursor.execute(GET_GOAL_DETAILS, (__unique_value,))
        val_tup = ('goal_description','amount', 'date', 'id')
        values = self.db_cursor.fetchall()
        details_list = []
        for val in values:
            details_dict = {
                val_tup[0]: val[0],
                val_tup[1]: val[1],
                val_tup[2]:val[2],
                val_tup[3]: val[3]
            }
            details_list.append(details_dict)
            
        return details_list
        
        
    def save_amount_details(self,email):
        """
        method return the save amount details
        """
        __unique_value  = self.__convert_to_unique(email)
        self.db_cursor.execute(SAVE_AMOUNT_INFO, (__unique_value,))
        values = self.db_cursor.fetchall()
        val_tup = ('save_amount', 'month')
        details_list = []
        for val in values:
            details_dict = {
                val_tup[0]: val[0],
                val_tup[1]: val[1]
            }
            details_list.append(details_dict)
            
        return details_list
    
    
    def get_credit_details(self, email):
        """
        method return the credit card details.
        """
        __unique_value  = self.__convert_to_unique(email)
        self.db_cursor.execute(GET_CREDIT_DETALS, (__unique_value,))
        values = self.db_cursor.fetchall()
        val_tup = ('credit_card', 'credited_amount', 'due_amount', 'paid_amount', 'month')
        details_list = []
        for val in values:
            details_dict = {
                val_tup[0]: val[0],
                val_tup[1]: val[1],
                val_tup[2]: val[2],
                val_tup[3]: val[3],
                val_tup[4]: val[4]
            }
            details_list.append(details_dict)
            
        return details_list