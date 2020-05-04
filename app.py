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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/shoestore.db'
app.config['SECRET_KEY']="all nighters are brutal"
database=SQLAlchemy(app)
login_manager= LoginManager()
login_manager.init_app(app)




@app.route('/')
def index():
    return render_template('index.html',Item_type="Shoe Store", items=['1','2','3'])



@app.route('/profile',methods=['POST'])
def remove_from_cart():
    request.form.get('next')
    item_id = request.form['item_id']
    cust_id = request.form['cust_id']
    
    deletion = Cart.delete().where(Cart.c.CUST_ID == cust_id).where(Cart.c.ITEM_ID == item_id) 
    deletion.compile().params
    connection = database.engine.connect()
    connection.execute(deletion) 
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    cust_ID = database.session.query(Customer.c.CUST_ID).filter(Customer.c.EMAIL == current_user.email).first()
    cust_ID = cust_ID[0]
   
    cart = database.session.query(Cart.c.ITEM_ID).filter(Cart.c.CUST_ID == cust_ID)

    shoe_cart = database.session.query(Shoes.c.SHOE_NAME)\
            .add_columns(Item.c.PRICE,
                    Shoes.c.SHOE_TYPE,
                    Item.c.ITEM_ID,
                    Item.c.BRAND,
                    Shoes.c.SHOE_DESC,
                    Cart.c.CUST_ID,
                    Cart.c.NUM_ITEM)\
                            .join(Item, Shoes.c.SHOE_ID == Item.c.ITEM_ID)\
                            .join(Cart, Shoes.c.SHOE_ID == Cart.c.ITEM_ID)\
                            .filter(Cart.c.CUST_ID == cust_ID)

    
    sock_cart =  database.session.query(Socks.c.SOCK_NAME)\
            .add_columns(Item.c.PRICE, 
                    Item.c.ITEM_ID,
                    Item.c.BRAND,
                    Socks.c.SOCK_DESC,
                    Cart.c.NUM_ITEM,
                    Cart.c.CUST_ID)\
                            .join(Item, Socks.c.SOCK_ID == Item.c.ITEM_ID)\
                            .join(Cart, Socks.c.SOCK_ID == Cart.c.ITEM_ID)\
                            .filter(Cart.c.CUST_ID == cust_ID)

    acc_cart = database.session.query(Accessory.c.ACC_NAME)\
            .add_columns(Item.c.PRICE, 
                    Item.c.ITEM_ID,
                    Item.c.BRAND,
                    Accessory.c.ACC_DESC,
                    Cart.c.NUM_ITEM,
                    Cart.c.CUST_ID)\
                            .join(Item, Accessory.c.ACC_ID == Item.c.ITEM_ID)\
                            .join(Cart, Accessory.c.ACC_ID == Cart.c.ITEM_ID)\
                            .filter(Cart.c.CUST_ID == cust_ID)
        
    user = database.session.query(Customer.c.EMAIL)\
            .add_columns(Customer.c.ADDRESS, 
                    Cust_Name.c.FNAME, 
                    Cust_Name.c.MNAME, 
                    Cust_Name.c.LNAME)\
                            .join(Cust_Name, Customer.c.CUST_ID == Cust_Name.c.CUST_ID)\
                            .filter(Customer.c.CUST_ID == cust_ID).first()

    return render_template('profile.html', cart=cart, shoe_cart=shoe_cart, acc_cart=acc_cart, sock_cart=sock_cart, user=user)





@app.route('/purchase', methods=["POST"])
def add_to_cart():
    request.form.get('next')
    if current_user.is_authenticated:
        item = request.form['itemid']
        quantity = request.form['quantity']
        cust_ID = database.session.query(Customer.c.CUST_ID).filter(Customer.c.EMAIL == current_user.email).first()
        
        val = database.session.query(Cart.c.CUST_ID).add_columns(Cart.c.ITEM_ID,Cart.c.NUM_ITEM).filter(Cart.c.ITEM_ID == item and Cart.c.CUST_ID == cust_ID).first()
        if val is None: 
            new = Cart.insert().values({Cart.c.CUST_ID:cust_ID[0], Cart.c.ITEM_ID:item,Cart.c.NUM_ITEM:quantity}) 
            new.compile().params 
            connection = database.engine.connect()
            connection.execute(new)  
        else: 
            new = Cart.update().where(Cart.c.CUST_ID == cust_ID[0]).where(Cart.c.ITEM_ID==item).values(NUM_ITEM = int(val[2])+int(quantity))
            new.compile().params
            connection = database.engine.connect()
            connection.execute(new)
    else:
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/logout',methods=['POST'])
def logout():
    request.form.get('next')
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
    request.form.get('next')
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

    return render_template('shoes.html',Item_type="Shoes", items=shoedisplay())

@app.route('/shoes',methods=["POST"])
def get_shoe():
    request.form.get('next')
    quantity = request.form['quantity']
    item_id = request.form['itemid']

    return redirect(url_for('shoes'))



@app.route('/socks')
def socks():    
    return render_template('socks.html',Item_type="Socks", items=sockdisplay())

@app.route('/socks',methods=['POST'])
def get_socks():
    request.form.get('next')
    quantity = request.form['quantity']
    item_id = request.form['itemid']
    return redirect(url_for('socks'))

@app.route('/accessories')
def Accessories():
    return render_template('accessories.html',Item_type="Accessories", items=accessorydisplay())

@app.route('/accessories',methods=["POST"])
def get_accessories():
    request.form.get('next')
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
        self.password = password


   

@login_manager.user_loader
def load_user(user_id):
    results = database.session.query(Customer.c.EMAIL).filter(Customer.c.EMAIL==user_id).first()
    user = User(results[0])
    
    return user




if __name__ == "__main__":
    app.run()
