from sqlalchemy import MetaData,  insert, create_engine
from create import customer, cust_name, payment_type, order, item, accessory, shoes, contains, cart, socks

from csv import DictReader 

metadata = MetaData()
engine=create_engine('sqlite:///shoestore.db')
connection= engine.connect()

with open("./csvfiles/Customter.csv","r") as customerdata:
    custreader = DictReader(customerdata)
    for row in custreader:
        ins = customer.insert().values(
                CUST_ID = row["Cust_ID"],
                EMAIL = row["Email"],
                PHONE_NUM= row["Phone_Num"],
                ADDRESS = row["Address"],
                PASSWORD = row["Password"],
                PAYMENT_TYPE = row["Payment_Type"])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/Cust_name.csv","r") as custname:
    reader = DictReader(custname)
    for row in reader:
        ins = cust_name.insert().values(
                CUST_ID = row["Cust_ID"],
                FNAME = row["FName"],
                MNAME = row["MName"],
                LNAME = row["LName"])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/payment_type.csv","r") as payment:
    reader = DictReader(payment)
    for row in reader:
        ins = payment_type.insert().values(
                CUST_ID = row["Cust_ID"],
                GIFTCARD = row["Giftcard"],
                DEBIT = row["Debit"],
                CREDIT = row["Credit"])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/order.csv","r") as orders:
    reader = DictReader(orders)
    for row in reader:
        ins= order.insert().values(
                CUST_ID = row["Cust_ID"],
                ORDER_ID = row["Order_ID"],
                ORDER_TYPE = row["Order_Type"],
                ORDER_DESCRIPTION = row['Order_Description'],
                ORDER_DATE = row['Order_Date'],
                PAYMENT_AMOUNT = row['Payment_Amount'])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/item.csv","r") as items:
    reader = DictReader(items)
    for row in  reader:
        ins = item.insert().values(
                ITEM_ID = row["Item_ID"],
                PRICE = row['Price'],
                BRAND = row['Brand'],
                TYPE = row['Type'])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/shoe.csv","r") as shoefile:
    reader = DictReader(shoefile)
    for row in reader:
        ins = shoes.insert().values(
                SHOE_ID = row['Shoe_ID'],
                SHOE_DESC = row['ShoeName'],
                SHOE_NAME = row['ShoeDescription'])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/accessories.csv","r") as accfile:
    reader = DictReader(accfile)
    for row in reader:
        ins = accessory.insert().values(
                ACC_ID = row['Acc_ID'],
                ACC_DESC = row['AccName'],
                ACC_NAME = row['AccDescription'])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/sock.csv","r") as sockfile:
    reader = DictReader(sockfile)
    for row in reader:
        ins = socks.insert().values(
                SOCK_ID = row['Sock_ID'],
                SOCK_DESC = row['SockName'],
                SOCK_NAME = row['SockDescription'])
        ins.compile().params
        result = connection.execute(ins)

with open("./csvfiles/cart.csv","r") as cartfile:
    reader = DictReader(cartfile)
    for row in reader:
        ins = cart.insert().values(
                CUST_ID = row['Cust_ID'],
                ITEM_ID = row['Item_ID'],
                NUM_ITEM = "1") 
        ins.compile().params
        result = connection.execute(ins)
