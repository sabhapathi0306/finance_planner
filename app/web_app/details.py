import hashlib
import os
import psycopg2
from app.web_app.common_utils import (
    GET_DEATILS, GET_STATUS,
    GET_STATMENT
)
from dotenv import load_dotenv,find_dotenv

class Details:
    
    @staticmethod
    def __db_connection():
        load_dotenv(find_dotenv())
        url = os.environ.get("DATABASE_URL")
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        return conn, cursor
    
    def __init__(self):
        self.db_connection, self.db_cursor = Details.__db_connection()

    def __convert_to_unique(self, string):
        hash_object = hashlib.sha256(string.encode())
        return hash_object.hexdigest()[:32]
    
    def get_details(self, email):
        try:
            # COURSOR = CONN.cursor()
            __unique_value  = self.__convert_to_unique(email)
            self.db_cursor.execute(GET_DEATILS, (__unique_value,))
            val_tup = self.db_cursor.fetchone()
            coum_tup = ('name', 'total_income', 'budgeted_income', 'save', 'planned_type', 'month')
            if val_tup is not None:
                details_dict = {coum_tup[i]: val_tup[i] for i in range(len(val_tup))}
                self.db_cursor.execute(GET_STATUS, (__unique_value, ))
                status_val_tup = self.db_cursor.fetchone()
                status_dict_tup= ('status', 'password')
                status_dict = {status_dict_tup[i]: status_val_tup[i] for i in range(len(status_val_tup))}
                details_dict.update(status_dict)
                return details_dict, True
        except Exception:
            raise
            self.db_connection.close()
            return {},False
        
    def get_expenses(self, email):
        """GET BUDGET LOGS"""
        __unique_value  = self.__convert_to_unique(email)
        self.db_cursor.execute(GET_STATMENT, (__unique_value,))
        val_tup = self.db_cursor.fetchall()
        coum_tup = ('category', 'description', 'spent_amount', 'date', 'remaining')
        lis  =[]
        for val in val_tup:
            deatils_dic = {
                coum_tup[0]: val[0],
                coum_tup[1]: val[1],
                coum_tup[2]: val[2],
                coum_tup[3]: val[3].strftime('%Y-%m-%d'),
                coum_tup[4]: val[4]
            }
            lis.append(deatils_dic)
            
        return lis
    
