from sqlalchemy import create_engine, MetaData, Table, Integer, Float, String, Column, ForeignKey, Unicode, DateTime
from datetime import datetime


metadata = MetaData()
engine = create_engine('sqlite:///shoestore.db')

customer = Table('CUSTOMER', metadata,
        Column('CUST_ID', Integer(),primary_key=True),
        Column('CNAME',  Unicode(50), nullable=False),
        Column('EMAIL', String(50), nullable=False, unique=True),
        Column('PHONE_NUM',  Integer()),
        Column('ADDRESS', Unicode(80), nullable=False),
        Column('PASSWORD', String(25), nullable=False),
        Column('PAYMENT_TYPE',String(16)))
 
cust_name = Table('CUST_NAME', metadata,
        Column('CUST_ID', Integer(), ForeignKey('CUSTOMER.CUST_ID'), primary_key=True ),
        Column('FNAME',String(25),nullable=False),
        Column('MNAME',String(25),nullable=True),
        Column('LNAME', String(25),nullable=False))

payment_type = ('PAYMENT_TYPE', metadata,
        Column('CUST_ID', Integer(), ForeignKey('CUSTOMER.CUST_ID'), primary_key=True),
        Column('GIFTCARD', String(16)),
        Column('DEBIT',  String(16)),
        Column('CREDIT',String(16)))

order = Table('ORDER', metadata,
        Column('CUST_ID', Integer(), ForeignKey('CUSTOMER.CUST_ID'), primary_key=True),
        Column('ORDER_ID', Integer(), primary_key=True),
        Column('ORDER_TYPE', Integer(), nullable=False),
        Column('ORDER_DESCRIPTION', String(50), nullable=False),
        Column('ORDER_DATE', DateTime(), default=datetime.now, nullable=False),
        Column('PAYMENT_AMOUNT', Float(), nullable=False))

item = Table('ITEM', metadata,
        Column('ITEM_ID', Unicode(20), primary_key=True),
        Column('PRICE', Float(8), nullable=False),
        Column('BRAND', String(50), nullable=False),
        Column('TYPE', String(10), nullable=False))

accessory = Table('ACCESSORY', metadata,
        Column('ACC_ID', Unicode(20), ForeignKey('ITEM.ITEM_ID'), primary_key=True),
        Column('ACC_DESC', String(100)),
        Column('ACC_NAME', String(50), nullable=False))

shoes = Table('SHOES', metadata,
        Column('SHOE_ID', Unicode(20), ForeignKey('ITEM.ITEM_ID'), primary_key=True),
        Column('SHOE_DESC', String(100)),
        Column('SHOE_NAME', String(50), nullable=False))

socks = Table('SOCKS', metadata,
        Column('SOCK_ID', Unicode(20), ForeignKey('ITEM.ITEM_ID'), primary_key=True),
        Column('SOCK_DESC', String(100)),
        Column('SOCK_NAME', String(50), nullable=False))

contains = Table('CONTAINS', metadata,
        Column('CUST_ID', Integer(), ForeignKey('CUSTOMER.CUST_ID'), primary_key=True),
        Column('ITEM_ID', Unicode(8), ForeignKey('ITEM.ITEM_ID'), primary_key=True))
        

cart = Table('CART', metadata,
        Column('CUST_ID', Integer(), ForeignKey('CUSTOMER.CUST_ID'), primary_key=True),
        Column('ITEM_ID', Unicode(8), ForeignKey('ITEM.ITEM_ID'), primary_key=True),
        Column('NUM_ITEM', Integer(), nullable=False))

metadata.create_all(engine)