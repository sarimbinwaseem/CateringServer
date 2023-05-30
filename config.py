import os


class Config:
	basedir = os.path.abspath(os.path.dirname(__file__))
	# SECRET_KEY = os.environ.get('SECRET_KEY')
	SECRET_KEY = "Geghinrthuisofwevefg56sfckies"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'customers.db')
	# print(os.path.join(basedir, 'database.db'))
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
