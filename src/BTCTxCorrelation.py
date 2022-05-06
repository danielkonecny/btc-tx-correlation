"""
BTC - Darkmarket Transaction Correlation
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import time

from src.ArgumentParser import parse_arguments
from src.DatabaseHandler import DatabaseHandler
from src.BlockchainHandler import BlockchainHandler
from src.CorrelationAnalyser import analyse_txs
from src.DataExporter import DataExporter


def create_block_height_datetime_table(
        database: DatabaseHandler,
        blockchain: BlockchainHandler,
        full_blockchain: bool = False
):
    """
    Fill auxiliary table for obtaining block times.
    :param database:
    :param blockchain:
    :param full_blockchain: Optionally download the whole blockchain (very slow).
    :return:
    """
    start_block_height = 0
    end_block_height = blockchain.get_best_height()
    if not full_blockchain:
        # Blocks that should contain transactions from dataset with padding on both sides just to be sure.
        start_block_height = 677001
        end_block_height = 708200

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


def correlate(database, blockchain, product_id, order_time, minutes_back=60, minutes_to_future=24 * 60):
    """
    Demonstration of correlation on a subset of orders.
    :param database:
    :param blockchain:
    :param product_id:
    :param order_time:
    :param minutes_back: Because of inconsistency of block timestamps, 1 hour in the past just to be sure.
    :param minutes_to_future: Search blocks one day to the future for the transaction.
    :return:
    """
    evaluation = []

    variants = database.get_variants(product_id)
    start_block_height, _ = database.block_height_datetime_at_datetime(order_time, -minutes_back)
    end_block_height, _ = database.block_height_datetime_at_datetime(order_time, minutes_to_future)
    txs = blockchain.get_txs_from_range(start_block_height, end_block_height)

    for variant in variants:
        price = database.get_price(variant[0], order_time)
        if price is not None:
            order_dict = {
                'product_id': product_id,
                'ordered_at': order_time,
                'variant_id': variant[0],
                'btc_price': price
            }
            evaluation += analyse_txs(order_dict, txs)

    return evaluation


def main():
    config, args = parse_arguments()
    database = DatabaseHandler(
        config['database']['name'],
        config['database']['user'],
        config['database']['password'],
        config['database']['host'],
        config['database']['port']
    )
    blockchain = BlockchainHandler()
    data_exporter = DataExporter('export.csv')

    create_block_height_datetime_table(database, blockchain, config['full_blockchain'])

    if args.order_count > 0:
        orders = database.get_orders(args.order_count)

        evaluation = []
        for product_id, order_time in orders:
            evaluation += correlate(database, blockchain, product_id, order_time, 60, 24 * 60)

        # data_exporter.export_data(evaluation)
        data_exporter.print_data(evaluation)

    else:
        evaluation = correlate(database, blockchain, args.product_id, args.order_time, 60, 24 * 60)

        # data_exporter.export_data(evaluation)
        data_exporter.print_data(evaluation)


if __name__ == "__main__":
    main()
