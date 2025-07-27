# inventory-system/app/products/logs.py

from ..models import InventoryLog
from .. import db
from datetime import datetime

def log_inventory_action(product_id, action, details, user_id):
    """Helper function to log an inventory action."""
    try:
        log_entry = InventoryLog(
            product_id=product_id,
            action=action,
            details=details,
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error logging action: {e}")