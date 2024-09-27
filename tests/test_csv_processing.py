import csv
import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import load_mappings, process_order_history, process_transfer_history
from datetime import datetime

@pytest.fixture
def sample_mappings():
    return load_mappings('mappings.csv')

def test_load_mappings():
    mappings = load_mappings('mappings.csv')
    assert len(mappings) > 0
    assert 'Source' in mappings[0]
    assert 'Platform A Field' in mappings[0]
    assert 'Universal Template Field' in mappings[0]

def test_process_order_history(sample_mappings):
    sample_order = {
        'Timestamp (UTC)': '2024-01-06 00:41:58.537916Z',
        'Order Type': 'market',
        'Side': 'buy',
        'Pair': 'BTCUSD',
        'Subtotal (USD)': '39.53',
        'Fee (USD)': '0.47',
        'Volume (BTC)': '0.00089506',
        'Price (USD)': '44,164.64',
        'Reference Code': 'XIB5DDWP'
    }
    result = process_order_history(sample_order, sample_mappings)
    assert isinstance(result['date'], datetime)
    assert result['sent_amount'] == 39.53
    assert result['sent_currency'] == 'USD'
    assert result['received_amount'] == 0.00089506
    assert result['received_currency'] == 'BTC'
    assert result['fee_amount'] == 0.47
    assert result['fee_currency'] == 'USD'
    assert 'XIB5DDWP' in result['description']

def test_process_transfer_history(sample_mappings):
    sample_transfer = {
        'Timestamp Initiated (UTC)': '2024-08-14 14:03:17.999976Z',
        'Asset': 'BTC',
        'Total Amount (BTC)': '-0.02123058',
        'Fee (BTC)': '0',
        'TXID': '9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10',
        'Reference Code': 'TXN5Y4HF'
    }
    result = process_transfer_history(sample_transfer, sample_mappings)
    assert isinstance(result['date'], datetime)
    assert result['sent_amount'] == 0.02123058
    assert result['sent_currency'] == 'BTC'
    assert result['fee_amount'] == 0
    assert result['fee_currency'] == 'BTC'
    assert result['tx_hash'] == '9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10'
    assert 'TXN5Y4HF' in result['description']
    # Load the mappings from the CSV file
    mappings = load_mappings('mappings.csv')

    # Load the sample order and transfer data from the resources directory
    with open('tests/resources/order.csv', 'r') as order_file:
        order_data = csv.DictReader(order_file)

    with open('tests/resources/transfer.csv', 'r') as transfer_file:
        transfer_data = csv.DictReader(transfer_file)

    # Convert the order data
    converted_orders = []
    for row in order_data:
        converted_orders.append(process_order_history(row, mappings))

    # Convert the transfer data
    converted_transfers = []
    for row in transfer_data:
        converted_transfers.append(process_transfer_history(row, mappings))

    # Combine the converted orders and transfers
    combined_data = converted_orders + converted_transfers

    # Get the fieldnames from the first dictionary in converted_orders and converted_transfers
    order_fieldnames = list(converted_orders[0].keys())
    transfer_fieldnames = list(converted_transfers[0].keys())

    # Combine the fieldnames into a single list
    fieldnames = list(set(order_fieldnames + transfer_fieldnames))

    # Dump the combined data to a CSV file
    with open('tests/output/combined.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

    # Assert that the converted data is correct
    # You can add assertions here to verify that the data was converted correctly
    assert len(combined_data) > 0
    
def test_convert_data():
    # Load the mappings from the CSV file
    mappings = load_mappings('mappings.csv')

    # Load the sample order and transfer data from the resources directory
    with open('tests/resources/order.csv', 'r') as order_file:
        order_data = csv.DictReader(order_file)

    with open('tests/resources/transfer.csv', 'r') as transfer_file:
        transfer_data = csv.DictReader(transfer_file)

    # Convert the order data
    converted_orders = []
    for row in order_data:
        converted_orders.append(process_order_history(row, mappings))

    # Convert the transfer data
    converted_transfers = []
    for row in transfer_data:
        converted_transfers.append(process_transfer_history(row, mappings))

    # Combine the converted orders and transfers
    combined_data = converted_orders + converted_transfers

    # Dump the combined data to a CSV file
    with open('tests/output/combined.csv', 'w', newline='') as output_file:
        fieldnames = combined_data[0].keys()
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

    # Assert that the converted data is correct
    # You can add assertions here to verify that the data was converted correctly
    assert len(combined_data) > 0