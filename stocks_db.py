import pandas as pd
import pyodbc
import sqlalchemy as sa

from secret_data import SERVER, DATABASE, USERNAME, PASSWORD

class Connection:

    def __init__(self, server=SERVER, database=DATABASE, username=USERNAME, password=PASSWORD):
        self._server = server
        self._database = database
        self._username = username
        self._password = password

        self._conn = self.connect()

    def connect(self):
        # Note that the SQL Server (mixed) authentication must be on to log-in with a UN/PW (and the server must be restarted to get that to stick)
        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self._server};DATABASE={self._database};UID={self._username};PWD={self._password};Encrypt=no'
        conn = pyodbc.connect(connection_string)
        return conn

    def query(self, query):
        cursor = self._conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


