import smtplib
from email.message import EmailMessage

def send_low_stock_email(product):
    msg = EmailMessage()
    msg['Subject'] = f'Low Stock Alert for {product.name}'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'admin@example.com'
    msg.set_content(f'Stock for {product.name} is low: {product.stock} remaining.')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('youremail@example.com', 'yourpassword')
            server.send_message(msg)
    except Exception as e:
        print("Email sending failed:", e)