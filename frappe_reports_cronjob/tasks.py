import frappe
from frappe.utils import now_datetime

def send_sales_finance_report():
    # Compose the email content
    email_content = 'Test email'
    # Replace 'recipient@example.com' with the recipient's email address
    recipient_email = "ahmedtouahria2001@gmail.com"
    print("send_sales_finance_report")
    # Send the email
    frappe.sendmail(
        recipients=[recipient_email],
        sender=None,  # Use the default sender configured in Frappe
        subject="Sales Finance Report",
        message=email_content,
        
    )
