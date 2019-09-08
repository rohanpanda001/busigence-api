#!flask/bin/python
from flask import Flask
from flask import request, jsonify
from flaskext.mysql import MySQL
import json
import pandas as pd

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'helloworld'
app.config['MYSQL_DATABASE_DB'] = 'busigence'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
mycursor =conn.cursor()


@app.route('/', methods=['GET'])
def home():
    return 'hello'

@app.route('/showDatabases', methods=['POST'])
def showDatabases():
    mycursor.execute("show databases")
    result = mycursor.fetchall()
    return json.dumps(result)

@app.route('/showTables', methods=['POST'])
def showTables():
    db = request.form['db']
    mycursor.execute("use "+ db)
    mycursor.execute("show tables")
    result = mycursor.fetchall()
    return json.dumps(result)


@app.route('/showRows', methods=['POST'])
def showAll():
    table = request.form['table']
    mycursor.execute("Select * from " + table)
    result = mycursor.fetchall()
    return json.dumps(result)


@app.route('/proccessJoin', methods=['POST'])
def proccessJoin():
    content = request.get_json()
    join_type = content['join_type']
    tableMap = content['tables']

    seperator = ', '
    customers = tableMap['customers']
    orders = tableMap['orders']

    df_a = pd.read_sql("Select " + seperator.join(customers) + " from customers", conn)
    df_b = pd.read_sql("Select " + seperator.join(orders) + " from orders",conn)
    
    df_c = pd.merge(df_a, df_b,on='CustomerID',how=join_type)
    response = df_c.to_dict()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)