"""-*- coding: utf-8 -*-
app
Stacy Yanagihara
Drew Gotshalk
Charnalyn Crivello
2020-04-09
"""
import sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/shoestore.db'
database=SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def login(name):
    return name


@app.route('/shoes')
def shoes():
    return render_template('shoes.html')

@app.route('/socks')
def socks():
    return render_template('socks.html')

@app.route('/accessories')
def accessories():
    return render_template('accessories.html')
if __name__ == "__main__":
    app.run()
