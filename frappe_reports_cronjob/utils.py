import frappe
from frappe.utils import now_datetime
from datetime import datetime

def calculate_turnover_of_month():
    current_month = frappe.utils.now_datetime().strftime("%Y-%m")
    turnover = frappe.db.sql("""
        SELECT SUM(amount) FROM `tabSalesInvoice`
        WHERE docstatus = 1 AND posting_date LIKE %s
    """, ("%{}%".format(current_month)))

    return turnover[0][0] if turnover else 0



def calculate_net_profit_of_month():
    current_month = now_datetime().strftime("%Y-%m")
    revenue = frappe.db.sql("""
        SELECT SUM(amount) FROM `tabSalesInvoice`
        WHERE docstatus = 1 AND posting_date LIKE %s
    """, ("%{}%".format(current_month)))

    expenses = frappe.db.sql("""
        SELECT SUM(amount) FROM `tabExpense`
        WHERE docstatus = 1 AND posting_date LIKE %s
    """, ("%{}%".format(current_month)))

    return (revenue[0][0] if revenue else 0) - (expenses[0][0] if expenses else 0)


def calculate_profit_margin():
    net_profit = calculate_net_profit_of_month()
    turnover = calculate_turnover_of_month()

    if turnover != 0:
        return (net_profit / turnover) * 100
    else:
        return 0


def get_total_sales_this_month():
    current_month = datetime.now().strftime("%Y-%m")
    total_sales_this_month = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "posting_date": ("like", f"{current_month}%")},
        count=True,
    )
    return total_sales_this_month



def get_total_sales_amount_this_month():
    current_month = datetime.now().strftime("%Y-%m")
    total_sales_this_month = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "posting_date": ("like", f"{current_month}%")},
        fields=["SUM(grand_total) as total_sales"],
    )[0].total_sales
    return total_sales_this_month


def get_new_customers_this_month():
    current_month = datetime.now().strftime("%Y-%m")
    new_customers = frappe.get_all(
        "Customer",
        filters={"creation": ("like", f"{current_month}%")},
        count=True,
    )
    return new_customers


def get_total_payments_received_this_month():
    current_month = datetime.now().strftime("%Y-%m")
    total_payments_received = frappe.get_all(
        "Payment Entry",
        filters={"docstatus": 1, "posting_date": ("like", f"{current_month}%")},
        fields=["SUM(paid_amount) as total_payments"],
    )[0].total_payments
    return total_payments_received

def get_total_unpaid_invoices():
    total_unpaid_invoices = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "outstanding_amount": (">", 0)},
        fields=["SUM(outstanding_amount) as total_unpaid"],
    )[0].total_unpaid
    return total_unpaid_invoices



def get_average_payment_time():
    avg_payment_time = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "due_date": (">", frappe.utils.now())},
        fields=["AVG(DATEDIFF(due_date, posting_date)) as avg_payment_time"],
    )[0].avg_payment_time
    return avg_payment_time