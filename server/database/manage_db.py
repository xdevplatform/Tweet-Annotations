import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Create a database connection to a SQLite database. """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return connection

def create_table(connection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param connection: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)
