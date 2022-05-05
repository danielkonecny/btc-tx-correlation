"""
BTC - Darkmarket Transaction Correlation
Module for argument parsing.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

from pathlib import Path
import json
import datetime

from argparse import ArgumentParser


def load_config(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)

    return data


def parse_arguments():
    parser = ArgumentParser(
        prog='BTC-Tx Correlation',
        description='Correlate transactions from Bitcoin blockchain with darkmarket purchases.'
    )
    parser.add_argument('config', type=str, help='Location of the configuration file.')
    parser.add_argument('--order_count', type=int, default=0, help='Number of orders to correlate.')
    parser.add_argument('--product_id', type=str, default="")
    parser.add_argument('--order_time', type=str, default="",
                        help='Format for example: 2021-10-14T16:03:55.693+00:00')

    args = parser.parse_args()

    config_file_path = Path(args.config)
    data = load_config(config_file_path)
    args.order_time = datetime.datetime.fromisoformat(args.order_time)

    return data, args
