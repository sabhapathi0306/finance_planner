import psycopg2
from app.web_app import app

# Create a single database connection
# def create_connection():
#     url = 'postgres://yztemeod:sQkQSjSkGy6UfMDf6Rz7jZq0zoQg81oy@salt.db.elephantsql.com/yztemeod'
#     return psycopg2.connect(url)

if __name__ == '__main__':
    app.run(debug=True)