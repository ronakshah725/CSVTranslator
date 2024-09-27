import pandas as pd

def validate_csv(file, expected_columns):
    df = pd.read_csv(file)
    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {', '.join(missing_columns)}")
    return df

def get_order_history_columns():
    return [
        'Reference Code', 'Timestamp (UTC)', 'Order Type', 'Side', 'Pair',
        'Subtotal (USD)', 'Fee (USD)', 'Volume (BTC)', 'Price (USD)'
    ]

def get_transfer_history_columns():
    return [
        'Reference Code', 'Account', 'Asset', 'Timestamp Initiated (UTC)',
        'Type', 'Direction', 'TXID', 'Total Amount (BTC)', 'Fee (BTC)'
    ]