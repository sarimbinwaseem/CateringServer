#!/bin/python

from flask import Flask, request #, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/test", methods = ["GET", "POST", "DELETE", "UPDATE"])
def test():
	return {"value": "OK"}, 200

@app.route("/signUp", methods = ["GET", "POST", "DELETE", "UPDATE"])
def signUp():

	if request.method != "POST":
		# request other than GET and POST
		return "", 101

	# Getting key
	# key = request.form.get("key")

	# Getting all required data.
	try:
		userInformation = []

		userInformation.append(request.args.get("username"))
		userInformation.append(request.args.get("email"))
		userInformation.append(request.args.get("fName"))
		userInformation.append(request.args.get("lName"))
		userInformation.append(request.args.get("password"))
		userInformation.append(request.args.get("address"))
		userInformation.append(request.args.get("phone"))
		print(userInformation)

		for data in userInformation:
			if data is None:
				raise AttributeError

	
	except ValueError as e:
		print(e)
		return "", 418
	except AttributeError as e:
		print(e)
		return "", 418

	except Exception as e:
		print(e)
		return "", 500

	else:
		# Checking for existing User.

		# Username Check
		person = Customer.query.filter_by(username = userInformation[0]).first()
		if person is not None:
			return "unameexists"
		
		person = Customer.query.filter_by(email = userInformation[1]).first()
		if person is not None:
			return "emailexists"

		person = Customer.query.filter_by(phone = userInformation[6]).first()
		if person is not None:
			return "phoneexists"

		########## CHECKS COMPLETED ######

		# if person DNE.

		db.session.add(Customer(
			username = userInformation[0],
			email = userInformation[1],
			firstName = userInformation[2],
			lastName = userInformation[3],
			password = userInformation[4],
			address = userInformation[5],
			phone = userInformation[6],
			)
		)
		db.session.commit()
		# deleteAll()
		return "signupgood", 200


@app.route("/login", methods = ["POST"])
def login():
	try:
		userInformation = []

		userInformation.append(request.args.get("uniqueaddress"))
		userInformation.append(request.args.get("password"))

		print(userInformation)

		for data in userInformation:
			if data is None:
				raise AttributeError

	except ValueError as e:
		print(e)
		return "", 418
	except AttributeError as e:
		print(e)
		return "", 418

	else:

		customer = return_customer(userInformation[0])
		if customer is None:
			return "irfa", 200 # ???? User not found

		if userInformation[1] == customer.password:
			return "alsi", 200 # Authorized Login Sequence Initiated

		else:
			return "icpw", 200 # Incorrect Password

# def deleteAll():
# 	del userInformation

def return_customer(uniqueaddress):
	customer = Customer.query.filter_by(username = uniqueaddress).first()
	if customer is not None:
		return customer

	customer = Customer.query.filter_by(email = uniqueaddress).first()
	if customer is not None:
		return customer

	customer = Customer.query.filter_by(phone = uniqueaddress).first()
	if customer is not None:
		return customer

	else:
		return None


class Customer(db.Model):
	customerID = db.Column("customerID", db.Integer, primary_key=True)
	username = db.Column("username", db.String(20), unique=True, nullable=False)
	email = db.Column("email", db.String(60), unique=True, nullable=False)

	firstName = db.Column("fName", db.String(20), nullable=False)
	lastName = db.Column("lName", db.String(20), nullable=False)

	password = db.Column("password", db.String(30), nullable=False)

	address = db.Column("address", db.String(60), nullable=False)
	phone = db.Column("phone", db.String(13), unique=True, nullable=True)
	creationTime = db.Column(db.DateTime(timezone = True), server_default = func.now())
	
	def __repr__(self):
		return f"Customer('{self.username}', '{self.email}', '{self.password}')"

if __name__ == "__main__":
	db.create_all()
	app.run("0.0.0.0", port = 4023, debug = True)
