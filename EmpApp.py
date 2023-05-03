from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'giantdb'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('index.html')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    uname = request.form['uname']
    address = request.form['address']

    insert_sql = "INSERT INTO giantdb VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:

        cursor.execute(insert_sql, (name, phone, email, uname, address))
        db_conn.commit()

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

