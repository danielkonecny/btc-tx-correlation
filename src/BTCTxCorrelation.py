"""
BTC - Darkmarket Transaction Correlation
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 29. 4. 2022
"""

from src.ArgumentParser import parse_arguments
from src.DatabaseHandler import DatabaseHandler


def main():
    config = parse_arguments()
    database = DatabaseHandler(
        config['database']['name'],
        config['database']['user'],
        config['database']['password'],
        config['database']['host'],
        config['database']['port']
    )

    select = "SELECT * FROM product__items LIMIT 10"

    results = database.read(select)
    for result in results:
        print(result)

    # create_database(database, config['db_import_dir'])


if __name__ == "__main__":
    main()
