"""
BTC - Darkmarket Transaction Correlation
Module for obtaining data from BTC blockchain with Blockbook API.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import requests


class BlockchainHandler:
    def __init__(self):
        self.url = "http://bazar.fit.vutbr.cz:3001/api/v2"

    def get_txs_from_range(self, first_block, last_block):
        """
        :param first_block:
        :param last_block: Transactions from last block are also included.
        :return:
        """
        print(f"Transactions from range of blocks: {first_block}-{last_block}.")

        txs = []

        for block_height in range(first_block, last_block + 1):
            block = requests.get(f"{self.url}/block/{block_height}").json()
            txs += block['txs']

        return txs

    def get_best_height(self):
        info = requests.get(f"{self.url}").json()
        best_height = info['blockbook']['bestHeight']
        return best_height

    def height_time_generator(self, start_height, end_height):
        for height in range(start_height, end_height + 1):
            block = requests.get(f"{self.url}/block/{height}").json()
            yield height, block['time']
