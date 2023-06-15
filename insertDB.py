#!/bin/python
from run import app, db, Customer, Dish, Order
app.app_context().push()
db.create_all()

def returnCustomer(id):
    person = Customer.query.filter_by(username = id).first()
    if person is None:
        person = Customer.query.filter_by(email = id).first()

    return person


r = input('''What to do: 
1=> Insert Dish
2=> Delete Customer
3=> Reset Password
4=> Reset Hardware
5=> Show all users
: ''')


if r == '1':
    dish_name = input("Dish Name: ")
    dish_price = input("Price: ")
    serving_capacity = input("Serving Capacity: ")

    db.session.add(Dish(dishName = dish_name,
        dishPrice = dish_price,
        servingCapacity = serving_capacity))
    db.session.commit()

elif r == '2':
    username = input("Customername to delete: ")
    user = returnCustomer(username)
    if user is None:
        print("Customer does not exist")
    else:
        db.session.delete(user)
        db.session.commit()

elif r == '3':
    us = input("Email: ")
    per = returnCustomer(us)
    
    if per is None:
        print("Customer does not exist")
    else:
        p = input("Enter New Password: ")
        per.password = bcrypt.generate_password_hash(p).decode()
        db.session.commit()

elif r == '4':
    us = input("Customername: ")
    
    per = returnCustomer(us)
    if per is None:
        print("Customer does not exist")
    else:
        per.uuid = per.hard = "None"
        db.session.commit()

elif r == '5':
    print()
    all = Customer.query.all()
    for a in all:
        print(a.username, a.email)