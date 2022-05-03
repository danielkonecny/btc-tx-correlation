"""
BTC - Darkmarket Transaction Correlation
Module for argument parsing.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 29. 04. 2022
"""

from pathlib import Path
import json

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
    args = parser.parse_args()

    config_file_path = Path(args.config)
    data = load_config(config_file_path)

    data['db_import_dir'] = Path(data['db_import_dir'])

    return data
