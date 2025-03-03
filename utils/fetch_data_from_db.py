import pymysql
from sshtunnel import SSHTunnelForwarder
from utils.db_config import *
import paramiko
import pandas as pd
import pymysql.connections
import sys
mypkey = paramiko.RSAKey.from_private_key_file("../tmp/ram_id_rsa", password='')



class DbConnection:

    def __init__(self, database):
        self.database = database
        self.tunnel = None
        self.connection = None

    def connect_to_db(self):
        try:
            assert self.database in ['prod', 'demo', 'stage', 'dev', 'demo_test', 'live_db']
            port = ''
            host = ''

            if self.database in ['prod', 'demo', 'demo_test', 'live_db']:
                self.tunnel = SSHTunnelForwarder((eval(self.database)['ssh_host'],
                                                  eval(self.database)['ssh_port']),
                                                 ssh_username=eval(self.database)['ssh_user'],
                                                 ssh_pkey=mypkey,
                                                 remote_bind_address=(
                                                     eval(self.database)['sql_hostname'],
                                                     eval(self.database)['sql_port']
                                                 ))
                self.tunnel.start()
                port = self.tunnel.local_bind_port
                host = '127.0.0.1'

            elif self.database in ['stage', 'dev']:
                port = eval(self.database)['port']
                host = eval(self.database)['host']

            self.connection = pymysql.connect(
                host=host,
                user=eval(self.database)['sql_username'],
                passwd=eval(self.database)['sql_password'],
                db=eval(self.database)['schema_name'],
                port=port,
                autocommit=True
            )
            return self.connection

        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            error_string = f"function connect_to_db, at line number {line_number}, error is {repr(e)}"
            return error_string

    def dispose(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("Disposed conn")
        if self.tunnel:
            self.tunnel.close()
            print("Disposed tunnel")



def fetch_sql_data(query, database):
    DB = DbConnection(database)

    try:
        conn = DB.connect_to_db()
        if not isinstance(conn, pymysql.connections.Connection):
            return pd.DataFrame(), conn
        cursor = conn.cursor()
        data = pd.read_sql_query(query, conn)
        cursor.close()

        DB.dispose()
        return data, True

    except Exception as e:
        DB.dispose()
        exc_type, _, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        error_string = f"function fetch_sql_data, at line number {line_number}, error is {repr(e)}"
        return pd.DataFrame(), error_string


def delete_sql_data(query, database):
    DB = DbConnection(database)

    try:
        conn = DB.connect_to_db()
        if not isinstance(conn, pymysql.connections.Connection):
            return pd.DataFrame(), conn
        cursor = conn.cursor()
        cursor.execute(query)
        deleted_count = cursor.rowcount
        cursor.close()

        DB.dispose()
        return deleted_count, True

    except Exception as e:
        DB.dispose()
        exc_type, _, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        error_string = f"function delete_sql_data, at line number {line_number}, error is {repr(e)}"
        return 0, error_string


def insert_sql_data(query, database):
    DB = DbConnection(database)

    try:
        conn = DB.connect_to_db()
        if not isinstance(conn, pymysql.connections.Connection):
            return pd.DataFrame(), conn
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()

        DB.dispose()
        return True

    except Exception as e:
        DB.dispose()
        exc_type, _, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        error_string = f"function insert_sql_data, at line number {line_number}, error is {repr(e)}"
        return error_string

# database = "stage"
# schema_name = "bs_stage_kb"
# query = "select * from bs_stage_kb.digitap_transactions_info where digitap_data_id=52660;"
# data, status = fetch_sql_data(query, database)
# print(data)