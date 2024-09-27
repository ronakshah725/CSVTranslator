from flask import Blueprint, request, jsonify
from app.utils import load_mappings, process_order_history, process_transfer_history
import csv
import io

bp = Blueprint('main', __name__)

mappings = load_mappings('mappings.csv')

@bp.route('/')
def index():
    return "Welcome to the CSV Translator API"

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        content = file.stream.read().decode('utf-8')
        csv_input = csv.DictReader(io.StringIO(content))
        preview = list(csv_input)[:5]  # First 5 rows for preview
        return jsonify({"columns": csv_input.fieldnames, "preview": preview})

@bp.route('/process', methods=['POST'])
def process_files():
    order_file = request.files.get('order_file')
    transfer_file = request.files.get('transfer_file')
    
    result = []
    
    if order_file:
        content = order_file.stream.read().decode('utf-8')
        csv_input = csv.DictReader(io.StringIO(content))
        for row in csv_input:
            result.append(process_order_history(row, mappings))
    
    if transfer_file:
        content = transfer_file.stream.read().decode('utf-8')
        csv_input = csv.DictReader(io.StringIO(content))
        for row in csv_input:
            result.append(process_transfer_history(row, mappings))
    
    return jsonify(result)