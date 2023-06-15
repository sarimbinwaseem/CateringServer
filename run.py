#!/bin/python

import datetime
from flask import Flask, request #, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch = True)
# https://flask-migrate.readthedocs.io/en/latest/index.html

@app.route("/", methods = ["GET", "POST", "DELETE", "UPDATE"])
def home():
	return {"value": "OK"}, 200

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
		data = request.get_json()
		userInformation = []

		userInformation.append(data.get("username"))
		userInformation.append(data.get("email"))
		userInformation.append(data.get("fName"))
		userInformation.append(data.get("lName"))
		userInformation.append(data.get("password"))
		userInformation.append(data.get("address"))
		userInformation.append(data.get("phone"))
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

		data = request.get_json()

		userInformation.append(data.get("uniqueaddress"))
		userInformation.append(data.get("password"))

		print("Data Recieved:", userInformation)

		for data in userInformation:
			if data is None:
				raise AttributeError

	except ValueError as e:
		print(e)
		return "Value Error", 200
	except AttributeError as e:
		print(e)
		return "None data", 200

	else:

		customer = return_customer(userInformation[0])
		if customer is None:
			return "irfa", 200 # ???? User not found

		if userInformation[1] == customer.password:
			return "alsi", 200 # Authorized Login Sequence Initiated

		else:
			return "icpw", 200 # Incorrect Password

@app.route("/neworder", methods = ["POST"])
def new_order():
	try:
		newOrder = []

		data = request.get_json()

		# UA = Unique Address i.e. phone,  | email, username
		newOrder.append(data.get("customerUA"))
		newOrder.append(data.get("deliveryDate"))
		newOrder.append(data.get("dishes"))

		print("Data Recieved:", newOrder)

		for data in newOrder:
			if data is None:
				raise AttributeError

	except ValueError as e:
		print(e)
		return "Value Error", 200
	except AttributeError as e:
		print(e)
		return "None data", 200

	except Exception as e:
		print(e)
		return "some error occured", 200

	else:
		customer = return_customer(newOrder[0])
		if customer is None:
			return "irfa"

		# FOR DISH
		dish = Dish.query.filter_by(dishID = newOrder[1]).first()

		date = convert_date(newOrder[2])

		db.session.add(Order(customer = customer.customerID,
							dishes = dish,
							deliveryDate = date))
		db.session.commit()

	return 1


@app.route("/newdish", methods = ["POST"])
def new_dish():
	try:
		newDish = []

		data = request.get_json()

		newDish.append(data.get("dishName"))
		newDish.append(data.get("dishPrice"))
		newDish.append(data.get("servingCapacity"))

		print("Data Recieved:", newDish)

		for data in newDish:
			if data is None:
				raise AttributeError

	except ValueError as e:
		print(e)
		return "Value Error", 200
	except AttributeError as e:
		print(e)
		return "None data", 200

	else:
		db.session.add(Dish(
			dishName = newDish[0],
			dishPrice = newDish[1],
			servingCapacity = newDish[2]
			))
		db.commit()

	return 1

def convert_date(rawdate) -> datetime.date:
	# Date
	# convert date to datetime format
	rawdate = newOrder[2].split('|') # yyyy|M|D
	date = datetime.date(*rawdate)
	return date

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

# Create Customer then Dishes then Orders
class Customer(db.Model):
	customerID = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(60), unique=True, nullable=False)

	firstName = db.Column(db.String(20), nullable=False)
	lastName = db.Column(db.String(20), nullable=False)

	password = db.Column(db.String(30), nullable=False)

	address = db.Column(db.String(60), nullable=False)
	phone = db.Column(db.String(13), unique=True, nullable=True)
	creationTime = db.Column(db.DateTime(timezone = True), server_default = func.now())
	
	# One Customer can have multiple orders
	orders = db.relationship('Order', backref='customer')

	def __repr__(self):
		return f"Customer('{self.username}', '{self.email}', '{self.password}')"

class Order(db.Model):
	orderID = db.Column("orderID", db.Integer, primary_key=True)
	# One Order can have one Customer
	customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"))
	
	# One Order can have multiple Dishes.
	dishes = db.Column(db.String, nullable = False)
	deliveryDate = db.Column(db.DateTime(timezone = True))

	# One Order can have one Rider
	riderID = db.Column(db.Integer, db.ForeignKey("rider.riderID"))

	def __repr__(self):
		return f"Order('{self.orderID}', '{self.customer}', '{self.deliveryDate}')"

class Dish(db.Model):
	dishID = db.Column("dishID", db.Integer, primary_key=True)
	dishName = db.Column("dishName", db.String(20), unique=True, nullable=False)
	dishPrice = db.Column("dishPrice", db.Integer, nullable=False)
	servingCapacity = db.Column("servingCapacity", db.Integer, nullable=False)

	# orderID = db.Column(db.Integer, db.ForeignKey("order.orderID"))

class Rider(db.Model):
	riderID = db.Column(db.Integer, primary_key=True)
	riderName = db.Column(db.String(20), unique=True, nullable=False)
	riderSalary = db.Column(db.Integer, nullable=False)
	 # = db.Column("servingCapacity", db.Integer, nullable=False)

	 # One Rider can have multiple orders
	todeliver = db.relationship('Order', backref='rider')

if __name__ == "__main__":
	# db.create_all()
	app.run("0.0.0.0", port = 4023, debug = True)
