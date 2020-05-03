"""-*- coding: utf-8 -*-
app
Stacy Yanagihara
Drew Gotshalk
Charnalyn Crivello
2020-04-09
"""
import sys
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(1, './database')
from create_store import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/shoestore.db'
database=SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html',Item_type="Shoe Store", items=['1','2','3'])


@app.route('/shoes')
def shoes():
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
    return redirect(url_for('socks'))



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







if __name__ == "__main__":
    app.run()
