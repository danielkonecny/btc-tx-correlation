"""
BTC - Darkmarket Transaction Correlation
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import pprint
import time

from src.ArgumentParser import parse_arguments
from src.DatabaseHandler import DatabaseHandler
from src.BlockchainHandler import BlockchainHandler


def create_block_height_datetime_table(
        database: DatabaseHandler,
        blockchain: BlockchainHandler,
        start_block_height: int,
        end_block_height: int
):
    database.create_block_height_time_table()

    current_height = database.get_height_from_table()

    if current_height > start_block_height:
        start_block_height = current_height + 1

    if current_height < end_block_height:
        print(f"Starting at {start_block_height} to reach {end_block_height}.")
        start_time = time.perf_counter()
        block_info = []
        size = 100
        for block_height, block_time in blockchain.height_time_generator(start_block_height, end_block_height):
            block_info.append((block_height, block_time))

            if block_height % size == 0:
                database.insert_heights_times(block_info)
                end_time = time.perf_counter()
                print(f"Processed {size} blocks in {end_time - start_time}, current height is {block_height}.")

                start_time = time.perf_counter()
                block_info = []


def main():
    config = parse_arguments()
    database = DatabaseHandler(
        config['database']['name'],
        config['database']['user'],
        config['database']['password'],
        config['database']['host'],
        config['database']['port']
    )
    blockchain = BlockchainHandler()

    # Fill auxiliary table for obtaining block times.
    start_height = 0
    end_height = blockchain.get_best_height()
    if not config['full_blockchain']:
        # Blocks that should contain transactions from dataset with padding on both sides just to be sure.
        start_height = 677001
        end_height = 708200
    create_block_height_datetime_table(database, blockchain, start_height, end_height)

    select = """
    SELECT
    ps.created_at AS ordered_at,
    pi.name AS product,
    pvi.name AS variant,
    ps.sales_delta * pvp.btc AS btc_price,
    ps.sales_delta * pvp.usd AS usd_price
FROM product__stats AS ps
JOIN product__items AS pi ON ps.product_id = pi.id
JOIN product__variant__items AS pvi on pi.id = pvi.product_id
JOIN product__variant__prices AS pvp on pvi.id = pvp.variant_id
WHERE ps.sales_delta != 0
LIMIT 1;
"""

    results = database.read(select)

    order = {
        'ordered_at': results[0][0],
        'btc_price': results[0][3]
    }

    # minutes_back = -60  # Because of inconsistency of block timestamps, 1 hour in the past just to be sure.
    minutes_back = 0
    start_block_height, _ = database.block_height_datetime_at_datetime(order['ordered_at'], minutes_back)
    # minutes_to_future = 24 * 60  # Search blocks one day to the future for the transaction.
    minutes_to_future = 0
    end_block_height, _ = database.block_height_datetime_at_datetime(order['ordered_at'], minutes_to_future)

    txs = blockchain.get_txs_from_range(start_block_height, end_block_height)
    pprint.pprint(txs)


if __name__ == "__main__":
    main()
