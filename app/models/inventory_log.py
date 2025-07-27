from .db import db
from datetime import datetime

class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    action = db.Column(db.String(50))  # e.g., 'sale', 'restock', 'return'
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="logs")
    user = db.relationship("User", backref="inventory_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "quantity": self.quantity,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }