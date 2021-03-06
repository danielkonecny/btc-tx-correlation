# Correlate Darkmarket Orders to BTC Txs

## Setup

1. Install necessary libraries from `requirements.txt` (to a virtual environment if necessary).
2. Add project directory to `PYTHONPATH` for relative imports to work. Or change the relative imports of source files to absolute imports according to your local directory structure.
3. Set database connection in `config.json` file.
4. Launch `src/BTCTxCorrelation.py` from the project root folder:
    * `python3 src/BTCTxCorrelation.py "config.json" --order_count=10` - demonstratively correlate any number of orders chosen from database.
    * `python3 src/BTCTxCorrelation.py "config.json" --product_id="6143260f-4637-5c33-9d80-af97233fb7ff" --order_time="2021-10-14T16:03:55.693+00:00"` - correlate a single order of a specific product ordered at given time.
5. This app needs data of block timestamps. You have to do one of the following:
   * Create the needed table with `data/block__height__datetime.sql` and import the blockchain data from `data/block__height__datetime.csv` file to it.
   * Launch the app, which will automatically create an auxiliary table to store block times with block heights. It only downloads blocks that correspond to the dataset timespan. To download the whole blockchain to the auxiliary table, set `full_blockchain` to true in `config.json`.
