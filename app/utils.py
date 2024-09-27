import csv
from datetime import datetime

def load_mappings(file_path):
    mappings = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mappings.append(row)
    return mappings

def process_order_history(order, mappings):
    is_buy = order['Side'].lower() == 'buy'
    return {
        'date': datetime.strptime(order['Timestamp (UTC)'], '%Y-%m-%d %H:%M:%S.%fZ'),
        'sent_amount': float(order['Subtotal (USD)']) if is_buy else float(order['Volume (BTC)']),
        'sent_currency': 'USD' if is_buy else 'BTC',
        'received_amount': float(order['Volume (BTC)']) if is_buy else float(order['Subtotal (USD)']),
        'received_currency': 'BTC' if is_buy else 'USD',
        'fee_amount': float(order['Fee (USD)']),
        'fee_currency': 'USD',
        'description': f"Reference Code: {order['Reference Code']}"
    }

def process_transfer_history(transfer, mappings):
    return {
        'date': datetime.strptime(transfer['Timestamp Initiated (UTC)'], '%Y-%m-%d %H:%M:%S.%fZ'),
        'sent_amount': abs(float(transfer['Total Amount (BTC)'])),
        'sent_currency': transfer['Asset'],
        'fee_amount': float(transfer['Fee (BTC)']),
        'fee_currency': transfer['Asset'],
        'description': f"Reference Code: {transfer['Reference Code']}",
        'tx_hash': transfer['TXID']
    }