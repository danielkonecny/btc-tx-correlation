"""
BTC - Darkmarket Transaction Correlation
Module for data export into CSV file.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import sys

import pandas as pd
from pathlib import Path


class DataExporter:
    def __init__(self, export_file_path):
        self.file_path = Path(export_file_path)
        self.df = None

    def export_data(self, data):
        self.df = pd.DataFrame(
            data,
            columns=['product_id', 'variant_id', 'tx_id', 'address', 'price_diff', 'heuristics']
        )
        self.df.to_csv(self.file_path, index=False)

    def print_data(self, data):
        self.df = pd.DataFrame(
            data,
            columns=['product_id', 'variant_id', 'tx_id', 'address', 'price_diff', 'heuristics']
        )
        self.df.to_csv(sys.stdout, index=False)
