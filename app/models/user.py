from .db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Add role field (Admin or Staff)
    role = db.Column(db.String(50), nullable=False, default='Staff')  # 'Admin' or 'Staff'

    def is_admin(self):
        return self.role.lower() == 'admin'

    def is_staff(self):
        return self.role.lower() == 'staff'
