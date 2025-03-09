import pandas as pd
import sqlalchemy as sa


class Database:
    def __init__(self, server, database, username=None, password=None):
        driver = "ODBC Driver 18 for SQL Server"
        driver = driver.replace(" ", "+")

        base_url = (
            f"mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes"
        )

        self._engine = sa.create_engine(base_url, fast_executemany=True)

