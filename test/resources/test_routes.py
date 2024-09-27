import pytest
from app import create_app, db
import io

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_upload_file(client):
    data = {'file': (io.BytesIO(b'Reference Code,Timestamp (UTC),Order Type,Side,Pair\n'), 'test.csv')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'columns' in response.json
    assert 'preview' in response.json

def test_process_files(client):
    order_data = io.BytesIO(b'Reference Code,Timestamp (UTC),Order Type,Side,Pair,Subtotal (USD),Fee (USD),Volume (BTC),Price (USD)\nXIB5DDWP,2024-01-06 00:41:58.537916Z,market,buy,BTCUSD,39.53,0.47,0.00089506,"44,164.64"')
    transfer_data = io.BytesIO(b'Reference Code,Account,Asset,Timestamp Initiated (UTC),Type,Direction,TXID,Total Amount (BTC),Fee (BTC)\nTXN5Y4HF,PS5KM7R6,BTC,2024-08-14 14:03:17.999976Z,OnChain,Outbound,9ad38309bdf5403075b14a03dc2083ecdbc28c2b3f25a21728430f888bef9b10,-0.02123058,0')
    
    data = {
        'order_file': (order_data, 'order.csv'),
        'transfer_file': (transfer_data, 'transfer.csv')
    }
    response = client.post('/process', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert len(response.json) == 2  # One order and one transfer