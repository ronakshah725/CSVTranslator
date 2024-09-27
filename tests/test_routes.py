import pytest
import sys
import os
import io
import json

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_upload_file(client):
    data = {'file': (io.BytesIO(b'Reference Code,Timestamp (UTC),Order Type,Side,Pair\n'), 'test.csv')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'columns' in json.loads(response.data)
    assert 'preview' in json.loads(response.data)

def test_process_files(client):
    order_data = io.BytesIO(b'Reference Code,Timestamp (UTC),Order Type,Side,Pair,Subtotal (USD),Fee (USD),Volume (BTC),Price (USD)\nXIB5DDWP,2024-01-06 00:41:58.537916Z,market,buy,BTCUSD,39.53,0.47,0.00089506,"44,164.64"')
    transfer_data = io.BytesIO(b'Reference Code,Account,Asset,Timestamp Initiated (UTC),Type,Direction,TXID,Total Amount (BTC),Fee (BTC)\nTXN5Y4HF,PS5KM7R6,BTC,2024-08-14 14:03:17.999976Z,OnChain,Outbound,9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10,-0.02123058,0')
    
    data = {
        'order_file': (order_data, 'order.csv'),
        'transfer_file': (transfer_data, 'transfer.csv')
    }
    response = client.post('/process', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert len(result) == 2  # One order and one transfer
    assert 'sent_amount' in result[0]
    assert 'sent_amount' in result[1]