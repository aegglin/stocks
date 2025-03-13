import pyodbc
import sqlalchemy as sa

from sqlalchemy.orm import Session

from secret_data import SERVER, DATABASE, USERNAME, PASSWORD

class Connection:

    def __init__(self, server=SERVER, database=DATABASE, username=USERNAME, password=PASSWORD):
        self._server = server
        self._database = database
        self._username = username
        self._password = password

        self._conn = self._connect_pyodbc()
        self._engine = self._sa_create_engine()
        self._session = self._sa_create_session()

    def _sa_create_engine(self, echo=False):
        driver = 'ODBC+Driver+18+for+SQL+Server'
        url = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={driver}&encrypt=no'
        return sa.create_engine(url, echo=echo)

    def _sa_create_session(self):
        return Session(self._engine)

    def _connect_pyodbc(self):
        # Note that the SQL Server (mixed) authentication must be on to log-in with a UN/PW (and the server must be restarted to get that to stick)
        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self._server};DATABASE={self._database};UID={self._username};PWD={self._password};Encrypt=no'
        conn = pyodbc.connect(connection_string)
        return conn

    def _query_pyodbc(self, query):
        cursor = self._conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


