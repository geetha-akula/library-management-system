# MAD-1 Project

project demonstration on library management system app


# Virtual environment creation

python -m venv env


# To activate virtual environment

env\Scripts\activate


# To deactivate virtual environment

deactivate


# To install flask

pip install flask

# To install Flask-SQLAlchemy

pip install Flask-SQLAlchemy


# To install matplotlib python library

pip install matplotlib


# To see the pip installations

pip freeze


# To write all the pip installation packages

pip freeze > requirements.txt


# To run the flask application

python app.py


# To create database models from terminal

python
from app import *
db.create_all()
exit()

