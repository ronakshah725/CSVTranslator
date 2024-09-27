import pytest
from app import create_app, db
from app.models import Mapping, UniversalTemplate
import pandas as pd

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_mapping_load(app):
    Mapping.load_mappings('mappings.csv')
    assert Mapping.query.count() > 0

def test_universal_template_from_order_history(app):
    order_data = {
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
    order = pd.Series(order_data)
    universal_entry = UniversalTemplate.from_order_history(order)
    assert universal_entry.sent_currency == 'USD'
    assert universal_entry.received_currency == 'BTC'
    assert universal_entry.fee_currency == 'USD'

def test_universal_template_from_transfer_history(app):
    transfer_data = {
        'Timestamp Initiated (UTC)': '2024-08-14 14:03:17.999976Z',
        'Asset': 'BTC',
        'Total Amount (BTC)': '-0.02123058',
        'Fee (BTC)': '0',
        'TXID': '9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10',
        'Reference Code': 'TXN5Y4HF'
    }
    transfer = pd.Series(transfer_data)
    universal_entry = UniversalTemplate.from_transfer_history(transfer)
    assert universal_entry.sent_currency == 'BTC'
    assert universal_entry.sent_amount == 0.02123058
    assert universal_entry.tx_hash == '9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10'