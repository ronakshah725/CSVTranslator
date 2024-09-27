import datetime
from app import db
import pandas as pd

class Mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(64))
    platform_a_field = db.Column(db.String(64))
    universal_template_field = db.Column(db.String(64))
    notes = db.Column(db.Text)

    @staticmethod
    def load_mappings(csv_file):
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            mapping = Mapping(
                source=row['Source'],
                platform_a_field=row['Platform A Field'],
                universal_template_field=row['Universal Template Field'],
                notes=row['Notes']
            )
            db.session.add(mapping)
        db.session.commit()

class UniversalTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    sent_amount = db.Column(db.Float)
    sent_currency = db.Column(db.String(10))
    received_amount = db.Column(db.Float)
    received_currency = db.Column(db.String(10))
    fee_amount = db.Column(db.Float)
    fee_currency = db.Column(db.String(10))
    net_worth_amount = db.Column(db.Float)
    net_worth_currency = db.Column(db.String(10))
    label = db.Column(db.String(64))
    description = db.Column(db.Text)
    tx_hash = db.Column(db.String(128))

    @classmethod
    def from_order_history(cls, order):
        is_buy = order['Side'].lower() == 'buy'
        return cls(
            date=datetime.strptime(order['Timestamp (UTC)'], '%Y-%m-%d %H:%M:%S.%fZ'),
            sent_amount=float(order['Subtotal (USD)']) if is_buy else float(order['Volume (BTC)']),
            sent_currency='USD' if is_buy else 'BTC',
            received_amount=float(order['Volume (BTC)']) if is_buy else float(order['Subtotal (USD)']),
            received_currency='BTC' if is_buy else 'USD',
            fee_amount=float(order['Fee (USD)']),
            fee_currency='USD',
            net_worth_amount=None,
            net_worth_currency=None,
            label=None,
            description=f"Reference Code: {order['Reference Code']}",
            tx_hash=None
        )

    @classmethod
    def from_transfer_history(cls, transfer):
        return cls(
            date=datetime.strptime(transfer['Timestamp Initiated (UTC)'], '%Y-%m-%d %H:%M:%S.%fZ'),
            sent_amount=abs(float(transfer['Total Amount (BTC)'])),
            sent_currency=transfer['Asset'],
            received_amount=None,
            received_currency=None,
            fee_amount=float(transfer['Fee (BTC)']),
            fee_currency=transfer['Asset'],
            net_worth_amount=None,
            net_worth_currency=None,
            label=None,
            description=f"Reference Code: {transfer['Reference Code']}",
            tx_hash=transfer['TXID']
        )

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'sent_amount': self.sent_amount,
            'sent_currency': self.sent_currency,
            'received_amount': self.received_amount,
            'received_currency': self.received_currency,
            'fee_amount': self.fee_amount,
            'fee_currency': self.fee_currency,
            'net_worth_amount': self.net_worth_amount,
            'net_worth_currency': self.net_worth_currency,
            'label': self.label,
            'description': self.description,
            'tx_hash': self.tx_hash
        }