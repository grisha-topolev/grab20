#app/__init__.py
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app: Flask = Flask(__name__)
app.config.from_object('app.config.Config')

db: SQLAlchemy = SQLAlchemy(app)
migrate: Migrate = Migrate(app, db)


from app import routes, models  # noqa