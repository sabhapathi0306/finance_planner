from flask import Flask

app = Flask(__name__)


from app.web_app import routes