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
mycursor = conn.cursor()


@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


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
    content = request.get_json()
    db = content['db']
    mycursor.execute("use " + db)
    mycursor.execute("show tables")
    result = mycursor.fetchall()
    return json.dumps(result)


@app.route('/showRows', methods=['POST'])
def showAll():
    content = request.get_json()
    table = content['table']
    mycursor.execute("Select * from " + table)
    result = mycursor.fetchall()
    return json.dumps(result)


@app.route('/proccessJoin', methods=['POST'])
def proccessJoin():
    content = request.get_json()
    joinType = content['joinType']
    primaryKey = content['primaryKey']
    tableMap = content['tables']

    seperator = ', '
    customers = tableMap['customers']
    orders = tableMap['orders']

    df_a = pd.read_sql(
        "Select " + seperator.join(customers) + " from customers", conn)
    df_b = pd.read_sql("Select " + seperator.join(orders) +
                       " from orders", conn)

    df_c = pd.merge(df_a, df_b, on=primaryKey, how=joinType)
    response = df_c.to_json(orient='index')
    return response


@app.route('/proccessSort', methods=['POST'])
def proccessSort():
    content = request.get_json()
    sortKey = content['sortKey']
    isAscending = content['isAscending']
    tableData = content['tableData']

    df = pd.DataFrame.from_dict(tableData)

    final_df = df.sort_values(by=sortKey, ascending=isAscending)
    response = final_df.to_json(orient='index')
    return response


if __name__ == '__main__':
    app.run(debug=True)
