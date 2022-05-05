"""
BTC - Darkmarket Transaction Correlation
Module for data analysis with correlation.
Organisation: Brno University of Technology - Faculty of Information Technology
Author: Daniel Konecny (xkonec75)
Date: 05. 05. 2022
"""

import datetime


def is_valid_tx(tx):
    # Ignore coinbase tx.
    if int(tx['valueIn']) == 0:
        # print("Ignoring - Coinbase TX.")
        return False

    return True


def is_valid_output(output, inputs):
    if 'addresses' not in output:
        # print("Ignoring - No output addresses.")
        return False

    if len(output['addresses']) != 1:
        # print("Ignoring - Too many output addresses.")
        return False

    for vin in inputs:
        if 'addresses' not in vin:
            continue

        if len(output['addresses']) != 1:
            continue

        if vin['addresses'][0] == output['addresses'][0]:
            # print("Ignoring - Output is returning funds to input address.")
            return False

    return True


def analyse_txs(order, txs):
    price_diff_thresh = 10
    evaluation = []

    for tx in txs:
        if not is_valid_tx(tx):
            continue

        time_diff = datetime.datetime.fromtimestamp(tx['blockTime'], tz=datetime.timezone.utc) - order['ordered_at']

        for output in tx['vout']:
            if not is_valid_output(output, tx['vin']):
                continue

            price_diff = int(output['value']) - order['btc_price']
            heuristics = time_diff.seconds // 60

            if 0 < price_diff < price_diff_thresh:
                evaluation.append({
                    'product_id': order['product_id'],
                    'variant_id': order['variant_id'],
                    'tx_id': tx['txid'],
                    'address': output['addresses'][0],
                    'price_diff': price_diff,
                    'heuristics': heuristics
                })

    return evaluation
