"""
BTC - Darkmarket Transaction Correlation
Module for database handling.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import sys
import psycopg2
from psycopg2 import OperationalError
import datetime

BLOCK_HEIGHT_TIME_TABLE = "block__height__datetime"


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
        except OperationalError as e:
            print(f"The error '{e}' occurred when connecting to DB.", file=sys.stderr)

    def execute(self, query: str) -> None:
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except OperationalError as e:
            print(f"The error '{e}' occurred when executing query:\n{query}", file=sys.stderr)

    def read(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred when executing query:\n{query}", file=sys.stderr)

    def create_block_height_time_table(self):
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {BLOCK_HEIGHT_TIME_TABLE}
        (block_height SERIAL PRIMARY KEY, block_time INTEGER NOT NULL)"""
        self.execute(create_table_query)

    def get_height_from_table(self):
        select = f"SELECT block_height FROM {BLOCK_HEIGHT_TIME_TABLE} ORDER BY block_height DESC LIMIT 1;"
        height = self.read(select)
        if len(height) == 0:
            height = 0
        else:
            height = height[0][0]
        return height

    def insert_height_time(self, height, time):
        insert = f"INSERT INTO block__height__datetime (block_height, block_time) VALUES ({height}, {time});"
        self.execute(insert)

    def insert_heights_times(self, block_info):
        block_info_str = ", ".join(["%s"] * len(block_info))
        insert = f"INSERT INTO block__height__datetime (block_height, block_time) VALUES {block_info_str};"
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert, block_info)
        except OperationalError as e:
            print(f"The error '{e}' occurred when executing insert query.", file=sys.stderr)

    def block_height_datetime_at_datetime(self, test_datetime, offset=0):
        seconds = (test_datetime + datetime.timedelta(minutes=offset)).timestamp()

        select = f"""SELECT block_height, block_time
        FROM {BLOCK_HEIGHT_TIME_TABLE}
        WHERE block_time < {seconds}
        ORDER BY block_time DESC
        LIMIT 1;"""

        block_height, block_timestamp = self.read(select)[0]
        block_datetime = datetime.datetime.fromtimestamp(block_timestamp, tz=datetime.timezone.utc)

        return block_height, block_datetime

    def get_orders(self, order_limit):
        select = f"""SELECT pi.id, ps.created_at
        FROM product__stats ps
        JOIN product__items pi on ps.product_id = pi.id
        WHERE sales_delta != 0
        LIMIT {order_limit};"""

        orders = self.read(select)
        return orders

    def get_variants(self, product_id):
        select = f"""SELECT pvi.id
        FROM product__items pi
        JOIN product__variant__items pvi on pi.id = pvi.product_id
        WHERE pi.id = '{product_id}';"""

        variants = self.read(select)
        return variants

    def get_price(self, variant_id, created_at):
        """
        :param variant_id:
        :param created_at:
        :return: Price of the variant in the time at satoshi.
        """
        sats_in_btc = 100_000_000
        select = f"""SELECT btc
        FROM product__variant__prices
        WHERE variant_id = '{variant_id}' AND created_at > '{created_at}'
        ORDER BY created_at
        LIMIT 1;"""

        price = int(self.read(select)[0][0] * sats_in_btc)
        return price
