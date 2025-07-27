from .db import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    barcode = db.Column(db.String(150))
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    threshold = db.Column(db.Integer, default=10)
    expiry_date = db.Column(db.Date)
