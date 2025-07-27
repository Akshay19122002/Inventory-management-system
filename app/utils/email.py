import smtplib
from email.mime.text import MIMEText

def send_low_stock_email(product, to_email):
    subject = f"⚠️ Low Stock Alert for {product.name}"
    body = (
        f"The product '{product.name}' (SKU: {product.sku}) is below the threshold.\n"
        f"Current stock: {product.quantity}"
    )

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = "your-email@gmail.com"
    message["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your-email@gmail.com", "your-app-password")  # Use App Password here
        server.sendmail("your-email@gmail.com", [to_email], message.as_string())
