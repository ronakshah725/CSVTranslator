from flask import request, jsonify
from app import app, db
from app.models import UniversalTemplate
import pandas as pd

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
    transfer_file = request.files.get('transfer_file')
    
    result = []
    
    if order_file:
        order_df = pd.read_csv(order_file)
        for _, row in order_df.iterrows():
            universal_entry = UniversalTemplate.from_order_history(row)
            db.session.add(universal_entry)
            result.append(universal_entry.to_dict())
    
    if transfer_file:
        transfer_df = pd.read_csv(transfer_file)
        for _, row in transfer_df.iterrows():
            universal_entry = UniversalTemplate.from_transfer_history(row)
            db.session.add(universal_entry)
            result.append(universal_entry.to_dict())
    
    db.session.commit()
    return jsonify(result)