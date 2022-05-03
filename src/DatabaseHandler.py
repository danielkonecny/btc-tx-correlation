"""
BTC - Darkmarket Transaction Correlation
Module for database handling.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 01. 05. 2022
"""

import psycopg2
from psycopg2 import OperationalError


class DatabaseHandler:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to PostgreSQL DB successful.")
        except OperationalError as e:
            print(f"The error '{e}' occurred.")

    def execute(self, query: str) -> None:
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully.")
        except OperationalError as e:
            print(f"The error '{e}' occurred.")

    def read(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")
