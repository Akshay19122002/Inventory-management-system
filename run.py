# File 1: inventory-system/run.py
# This is the main entry point. It creates the app and makes it available to Flask.

from app import create_app, db
# Make sure to import all your models here so Flask-Migrate can see them
from app.models import User, Product, InventoryLog 

# Create the Flask app instance using your factory
app = create_app()

# This is a helpful command for debugging in the Flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'InventoryLog': InventoryLog}

if __name__ == '__main__':
    # This block only runs when you execute 'python run.py' directly
    app.run(debug=True)