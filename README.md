# Inventory System

This project is an inventory management system built using Flask and SQLAlchemy. It provides functionalities for user authentication and product management, allowing users to log in, register, and manage their inventory effectively.

## Project Structure

```
inventory-system/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # SQLAlchemy models
│   ├── auth/                 # Authentication (login/register)
│   │   ├── routes.py
│   │   ├── forms.py
│   ├── products/             # Product CRUD
│   │   ├── routes.py
│   │   ├── forms.py
│   ├── templates/            # HTML templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   ├── static/               # Static files (CSS/JS)
│       ├── css/
│       ├── js/
├── migrations/               # DB migrations (if using Flask-Migrate)
├── .env                      # Store secret key, DB URL
├── config.py                 # Config class (for secret key, DB)
├── run.py                    # Entry point (flask run)
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd inventory-system
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

5. **Run the application:**
   ```
   python run.py
   ```

## Usage

- Navigate to `http://localhost:5000` in your web browser.
- Use the login page to access your account or register a new account.
- Once logged in, you can manage your inventory through the dashboard.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.