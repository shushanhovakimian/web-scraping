from io import BytesIO
import pandas as pd
import psycopg2.extras as extras
import psycopg2
from datetime import datetime, date
from sqlalchemy import create_engine
import time
import subprocess


# setting credentials like this is not the best option, but it make code more configurable
DB_NAME = "postgres"
DB_PASSWORD = "admin"
DB_USER = "user"
DB_HOST = "local_pgdb"
DB_PORT = 5432


def db_connect(host=None, port=None, database=None, user=None, password=None):
    """create database connection"""
    try:
        connection = psycopg2.connect(host=host,
                                      port=port,
                                      database=database,
                                      user=user,
                                      password=password)
        print("connected successfully")
        return connection
    except Exception as error:
        print(type(error))
        print(error)

def year_to_age(birthday):
    today = date.today()
    diff = today.year - birthday.year
    if birthday.month > today.month:
        if birthday.day > today.day:
            return diff - 1
        else:
            return diff
    return diff - 1


def get_existing_ids(table):
    """get existing ids from database to filter out repeated ids"""

    connect = db_connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    connect.autocommit = True
    cursor = connect.cursor()
    sql = f"""SELECT user_id from {table}"""
    cursor.execute(sql)
    values = cursor.fetchall()
    connect.close()

    return values


def insert_values(dataframe, table):
    """import data to database"""

    conn = db_connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    tuples = [tuple(x) for x in dataframe.to_numpy()]

    cols = ','.join(list(dataframe.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


# this is other option to insert, but not used in our project
def insert(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, data=None):
    con_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    db = create_engine(con_string)
    con = db.connect()
    try:
        data.to_sql('users_info', con=con, if_exists='append', index=False)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":

#    files = get_list_of_files(bucket="stagingarea")
#    output = get_and_merge_files(files_to_process=files, bucket="stagingarea")
#    if output is not None:
#        insert_values(output, table="users_info")






