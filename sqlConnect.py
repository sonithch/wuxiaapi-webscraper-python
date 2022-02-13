import mysql.connector
from mysql.connector import Error
import pandas as pd
import os


sqlHost = str(os.environ.get("SQLHost"))
sqlUser = str(os.environ.get("SQLUser"))
sqlPassword = str(os.environ.get("SQLPassword"))



def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=sqlHost,
            user=sqlUser,
            passwd=sqlPassword,
            db="wuxiaapp",
            ssl_ca="/etc/ssl/cert.pem"
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def insertOrUpdateToTable(connection, table: str, values: tuple, columns: str):
    cursor = connection.cursor()
    try:
        query = '''
            REPLACE INTO {0} {1}
            VALUES {2}
            '''.format(table, columns, values)

        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")
