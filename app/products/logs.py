# app/products/logs.py

from app.models import InventoryLog, db
from datetime import datetime

def log_inventory_action(product_id, user_id, action, quantity):
    """
    Save a new inventory action log.
    """
    log = InventoryLog(
        product_id=product_id,
        user_id=user_id,
        action=action,
        quantity=quantity,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
