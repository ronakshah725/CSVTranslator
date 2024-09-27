# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Default mappings
default_order_mapping = {
    "Date": "timestamp",
    "Type": "side",
    "Price": "price",
    "Amount": "amount",
    "Total": "total"
}

default_transaction_mapping = {
    "Date": "timestamp",
    "Type": "type",
    "Asset": "asset",
    "Amount": "amount",
    "TransactionID": "txid"
}

@app.route('/')
def index():
    return render_template('index.html',
                           order_mapping=json.dumps(default_order_mapping),
                           transaction_mapping=json.dumps(default_transaction_mapping))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        df = pd.read_csv(file)
        return jsonify({"columns": df.columns.tolist(), "preview": df.head().to_dict('records')})

@app.route('/process', methods=['POST'])
def process_files():
    order_file = request.files.get('order_file')
    transaction_file = request.files.get('transaction_file')
    order_mapping = json.loads(request.form.get('order_mapping'))
    transaction_mapping = json.loads(request.form.get('transaction_mapping'))
    
    result = {}
    
    if order_file:
        order_df = pd.read_csv(order_file)
        processed_orders = process_data(order_df, order_mapping)
        result['orders'] = processed_orders.to_dict('records')
    
    if transaction_file:
        transaction_df = pd.read_csv(transaction_file)
        processed_transactions = process_data(transaction_df, transaction_mapping)
        result['transactions'] = processed_transactions.to_dict('records')
    
    return jsonify(result)

def process_data(df, mapping):
    return df.rename(columns=mapping)[list(mapping.values())]

if __name__ == '__main__':
    app.run(debug=True)