import frappe
from frappe.utils import now_datetime
from frappe_reports_cronjob.utils import *

def send_sales_finance_report():
    # Compose the email content
    # Replace 'recipient@example.com' with the recipient's email address
    recipient_email = "ahmedtouahria2001@gmail.com"
    print("send_sales_finance_report")
    unpaid=get_total_unpaid_invoices()
    average_payment= get_average_payment_time()
    get_total_payments=get_total_payments_received_last_month()
    calculate_net_profit = calculate_net_profit_of_month()
    chiffre_d_affaires_du_mois = calculate_chiffre_d_affaires_du_mois()
    profit_margin = calculate_profit_margin()
    get_total_sales_count=get_total_sales_count_this_month()
    get_total_sales_amount=get_total_sales_amount_this_month()
    get_new_customers_count=get_new_customers_count_this_month()
    payments_received=get_total_payments_received()
    unpaid_invoices=get_total_unpaid_invoices()
    email_content = f'profit_margin = {profit_margin} % get_average_payment_time = {average_payment},get_total_unpaid_invoices = {unpaid},get_total_payments = {get_total_payments} , calculate_net_profit ={calculate_net_profit} , chiffre_d_affaires_du_mois ={chiffre_d_affaires_du_mois}'
    email_content+=f"get_total_sales_count = {get_total_sales_count} , get_total_sales_amount = {get_total_sales_amount} , get_new_customers_count = {get_new_customers_count} "
    email_content+=f"payments_received = {payments_received} , unpaid_invoices = {unpaid_invoices} "

    print(email_content)
    # Send the email
    """ frappe.sendmail(
        recipients=[recipient_email],
        sender=None,  # Use the default sender configured in Frappe
        subject="Sales Finance Report",
        message=email_content,
        
    ) """

def send_stock_report():
    # Compose the email content
    recipient_email = "ahmedtouahria2001@gmail.com"
    print("send_stock_report")
    initial_stock_count = get_initial_stock_count()
    stock_end_of_month=get_initial_stock_count_end_of_month()
    total_orders_value = get_total_orders_value()
    total_orders_count=get_total_orders_count()
    average_time=calculate_average_delivery_time()
    email_content = f"initial_stock_count = {initial_stock_count} \n"
    email_content += f"total_orders_value = {total_orders_value}\n"
    email_content += f"stock_end_of_month = {stock_end_of_month}\n"
    email_content += f"total_orders_count = {total_orders_count}\n"
    email_content += f"average_time = {average_time}\n"
    print(email_content)
    # Send the email
    """ frappe.sendmail(
        recipients=[recipient_email],
        sender=None,  # Use the default sender configured in Frappe
        subject="Sales Finance Report",
        message=email_content,
        
    ) """

def send_production_report():
    # Compose the email content
    recipient_email = "ahmedtouahria2001@gmail.com"
    print("send_production_report")
    total_products_manufactured = get_total_products_manufactured()
    total_production_cost = get_total_price_for_manufactured_products()
    average_time = get_average_production_time_per_product()
    email_content = f"total_products_manufactured = {total_products_manufactured} \n"
    email_content += f"total_production_cost = {total_production_cost} \n"
    email_content += f"average_time = {average_time} \n"
    print(email_content)
    # Send the email
    """ frappe.sendmail(
        recipients=[recipient_email],
        sender=None,  # Use the default sender configured in Frappe
        subject="Sales Finance Report",
        message=email_content,
        
    ) """
