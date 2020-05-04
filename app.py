"""-*- coding: utf-8 -*-
app
Stacy Yanagihara
Drew Gotshalk
Charnalyn Crivello
2020-04-09
"""
import sys
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(1, './database')
from create_store import *
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/shoestore.db'
app.config['SECRET_KEY']="all nighters are brutal"
database=SQLAlchemy(app)
login_manager= LoginManager()
login_manager.init_app(app)




@app.route('/')
def index():
    

    return render_template('index.html',Item_type="Shoe Store", items=['1','2','3'])



@app.route('/profile')
def profile():
    
    cart = database.session.
    
    return render_template('profile.html')


@app.route('/logout',methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/logout')
def logout_null():
    
    return redirect(url_for('index'))


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return render_template('index.html', Item_type="Shoe Store", items=[])
    else: 
        return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_info(): 
    username = request.form['user']
    password = request.form['pass']
    user = User(username,password)
    result = database.session.query(Customer.c.EMAIL).add_column(Customer.c.PASSWORD).filter(Customer.c.EMAIL == username).first()
    if user.email == result[0] and user.password == result[1]:
        login_user(user,True)
        
        return render_template("index.html", Item_type="Shoe Store", items=[])
    return render_template('login.html')


      

@app.route('/shoes')
def shoes():
    #if 'username' in session 
    return render_template('shoes.html',Item_type="Shoes", items=shoedisplay())

@app.route('/shoes',methods=["POST"])
def get_shoe():
    quantity = request.form['quantity']
    item_id = request.form['itemid']

    return redirect(url_for('shoes'))



@app.route('/socks')
def socks():    
    return render_template('socks.html',Item_type="Socks", items=sockdisplay())

@app.route('/socks',methods=['POST'])
def get_socks():
    quantity = request.form['quantity']
    item_id = request.form['itemid']
    return redirect(url_for('socks'))

@app.route('/accessories')
def Accessories():
    return render_template('accessories.html',Item_type="Accessories", items=accessorydisplay())

@app.route('/accessories',methods=["POST"])
def get_accessories():
    quantity = request.form['quantity']
    item_id = request.form['itemid']
    return redirect(url_for('accessories'))






def shoedisplay():
    a_query = database.session.query(Shoes.c.SHOE_NAME)\
            .add_columns(Item.c.PRICE,
                    Shoes.c.SHOE_TYPE,
                    Item.c.BRAND,
                    Item.c.ITEM_ID)\
            .add_column(Shoes.c.SHOE_DESC)\
            .filter(Item.c.ITEM_ID == Shoes.c.SHOE_ID)
    return a_query


def sockdisplay(): 
    a_query = database.session.query(Socks.c.SOCK_NAME)\
            .add_columns(Item.c.PRICE,
                    Item.c.BRAND,
                    Item.c.ITEM_ID)\
            .add_column(Socks.c.SOCK_DESC)\
            .filter(Item.c.ITEM_ID == Socks.c.SOCK_ID)
    return a_query


def accessorydisplay():
    a_query = database.session.query(Accessory.c.ACC_NAME)\
            .add_columns(Item.c.PRICE,
                    Item.c.BRAND,
                    Item.c.ITEM_ID)\
            .add_column(Accessory.c.ACC_DESC)\
            .filter(Item.c.ITEM_ID == Accessory.c.ACC_ID)
    return a_query


    
class User(UserMixin):
    def __init__(self,username, password=None):
        self.id = username
        self.email = username
        self.username = username
        self.password_hash = password 
        self.password = password


   

@login_manager.user_loader
def load_user(user_id):
    results = database.session.query(Customer.c.EMAIL).filter(Customer.c.EMAIL==user_id).first()
    user = User(results[0])
    
    return user




if __name__ == "__main__":
    app.run()
