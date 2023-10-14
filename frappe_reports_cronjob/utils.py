import frappe
from frappe.utils import now_datetime
from datetime import datetime, timedelta
from frappe.utils import get_datetime
from frappe.utils import nowdate, add_days, get_first_day, get_last_day


def calculate_chiffre_d_affaires_du_mois():
    current_datetime = now_datetime()
    start_date = get_first_day(current_datetime)
    end_date = get_last_day(current_datetime)

    total_revenue = frappe.get_all("Sales Invoice", filters={
        "posting_date": ["between", [start_date, end_date]],
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(grand_total) as total_revenue"])[0].total_revenue or 0

    return total_revenue

def calculate_net_profit_of_month():
    """
    Calculate the net profit of the current month.

    Returns:
        float: The net profit of the current month.
    """

    start_date = frappe.utils.get_datetime().replace(day=1)
    end_date = frappe.utils.get_datetime().replace(day=31)

    total_revenue = frappe.get_all("Sales Invoice", filters={
        "posting_date": ["between", (start_date, end_date)]
    }, fields=["total"])
    print(total_revenue)
    total_expenses = frappe.get_all("Purchase Invoice", filters={
        "posting_date": ["between", (start_date, end_date)]
    }, fields=["total"])
    print(total_expenses)
    sum_a = sum(item['total'] for item in total_revenue)

# Calculate the sum of 'total' values in list 'b'
    sum_b = sum(item['total'] for item in total_expenses)

    # Subtract the sum of 'b' from the sum of 'a'
    result = sum_a - sum_b

    return result
def calculate_profit_margin():
    net_profit = calculate_net_profit_of_month()
    turnover = calculate_chiffre_d_affaires_du_mois()

    if turnover != 0:
        result =(net_profit / turnover) * 100
        return float(result)
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


def get_total_payments_received_last_month():
    """
    Return the total payments received in the last month.
    """

    current_date = nowdate()
    last_month_start = get_first_day(add_days(current_date, -30))
    last_month_end = get_last_day(add_days(current_date, -1))

    payments = frappe.get_all("Payment Entry", filters={
        "payment_type": "Receive",
        "posting_date": ["between", (last_month_start, last_month_end)]
    })

    total_payments = 0

    for payment in payments:
        payment_entry = frappe.get_doc("Payment Entry", payment["name"])
        if payment_entry and payment_entry.paid_amount_after_tax:
            total_payments += payment_entry.paid_amount_after_tax

    return total_payments
def get_total_unpaid_invoices():
    total_unpaid_invoices = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "outstanding_amount": (">", 0)},
        fields=["SUM(outstanding_amount) as total_unpaid"],
    )
    unpaid = total_unpaid_invoices[0].total_unpaid
    return unpaid if unpaid is not None else 0



def get_average_payment_time():
    avg_payment_time = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 1, "due_date": (">", frappe.utils.now())},
        fields=["AVG(DATEDIFF(due_date, posting_date)) as avg_payment_time"],
    )[0].avg_payment_time
    return avg_payment_time if avg_payment_time is not None else 0



# indicateur des clients

def get_total_sales_count_this_month():
    current_datetime = now_datetime()
    start_date = get_first_day(current_datetime)
    end_date = get_last_day(current_datetime)

    sales_invoices = frappe.get_all("Sales Invoice", filters={
        "posting_date": ["between", [start_date, end_date]],
        "docstatus": 1  # Include only submitted documents
    })

    total_sales_count = len(sales_invoices)

    return total_sales_count

def get_total_sales_amount_this_month():
    current_datetime = now_datetime()
    start_date = get_first_day(current_datetime)
    end_date = get_last_day(current_datetime)

    total_sales_amount = frappe.get_all("Sales Invoice", filters={
        "posting_date": ["between", [start_date, end_date]],
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(grand_total) as total_sales_amount"])[0].total_sales_amount or 0

    return total_sales_amount

def get_new_customers_count_this_month():
    current_datetime = now_datetime()
    start_date = get_first_day(current_datetime)
    end_date = get_last_day(current_datetime)

    new_customers = frappe.get_all("Customer", filters={
        "creation": ["between", [start_date, end_date]]
    })

    new_customers_count = len(new_customers)

    return new_customers_count

# payment

def get_total_payments_received():
    # Get the sum of paid amounts from Payment Entry documents
    total_payments = frappe.get_all("Payment Entry", filters={
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(paid_amount) as total_payments"])[0].total_payments or 0

    return total_payments


def get_total_unpaid_invoices():
    # Get the sum of outstanding amounts from Sales Invoice documents
    total_unpaid_invoices = frappe.get_all("Sales Invoice", filters={
        "docstatus": 1,  # Include only submitted documents
        "outstanding_amount": (">", 0)  # Filter for invoices with outstanding amounts
    }, fields=["SUM(outstanding_amount) as total_unpaid_invoices"])[0].total_unpaid_invoices or 0

    return total_unpaid_invoices


#============ stock ==================

def get_initial_stock_count():
    # Replace "Item" with the appropriate DocType representing your inventory items
    stock_entries = frappe.get_all("Stock Ledger Entry", filters={
        "posting_date": ("<", get_first_day(frappe.utils.now_datetime())),
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(actual_qty) as initial_stock_count"])

    return stock_entries[0].initial_stock_count or 0

def get_initial_stock_count_end_of_month():
    from datetime import date
    from dateutil.relativedelta import relativedelta

    # Calculate the first day of the current month
    today = date.today()
    first_day_of_current_month = today.replace(day=1)

    # Calculate the last day of the previous month (end of the current month)
    end_of_last_month = first_day_of_current_month - relativedelta(days=1)

    # Query Stock Ledger Entry records with a posting date before the end of the current month
    stock_entries = frappe.get_all("Stock Ledger Entry", filters={
        "posting_date": ("<=", end_of_last_month),
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(actual_qty) as initial_stock_count"])

    return stock_entries[0].initial_stock_count or 0
def get_final_stock_count():
    # Replace "Item" with the appropriate DocType representing your inventory items
    stock_entries = frappe.get_all("Stock Entry", filters={
        "posting_date": ("<=", get_last_day(frappe.utils.now_datetime())),
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(actual_qty) as final_stock_count"])

    return stock_entries[0].final_stock_count or 0


#Indicateurs d'Approvisionnement:

def get_total_orders_count():
    # Replace "Purchase Order" with the appropriate DocType representing your purchase orders
    orders = frappe.get_all("Purchase Order", filters={
        "docstatus": 1  # Include only submitted documents
    })

    return len(orders)

def get_total_orders_value():
    # Replace "Purchase Order" with the appropriate DocType representing your purchase orders
    orders = frappe.get_all("Purchase Order", filters={
        "docstatus": 1  # Include only submitted documents
    }, fields=["SUM(grand_total) as total_orders_value"])

    return orders[0].total_orders_value or 0

def calculate_average_delivery_time():
    total_delivery_time = timedelta()
    total_orders = 0

    # Query Sales Orders
    sales_orders = frappe.get_all("Sales Order", filters={"docstatus": 1}, fields=["transaction_date", "delivery_date"])

    for order in sales_orders:
        transaction_date = order.transaction_date
        delivery_date = order.delivery_date

        if transaction_date and delivery_date:
            delivery_time = delivery_date - transaction_date
            total_delivery_time += delivery_time
            total_orders += 1

    if total_orders > 0:
        average_delivery_time = total_delivery_time / total_orders
        return average_delivery_time
    else:
        return 0
# production

def get_total_products_manufactured():
    total_manufactured = 0
    # Query Stock Entry records with purpose "Manufacture" and status "Submitted"
    stock_entries = frappe.get_all("Stock Entry",
        filters={"purpose": "Manufacture", "docstatus": 1}  # 1 for Submitted
    )

    for stock_entry in stock_entries:
        for item in stock_entry.get("items"):
            if item.get("is_finished_item") == 1:  # 1 for True in Frappe/ERPNext
                total_manufactured += item.get("qty")

    return total_manufactured

def get_total_price_for_manufactured_products():
    total_price = 0
    # Query Stock Entry records with purpose "Manufacture" and status "Submitted"
    stock_entries = frappe.get_all("Stock Entry",
        filters={"purpose": "Manufacture", "docstatus": 1}  # 1 for Submitted
    )

    for stock_entry in stock_entries:
        for item in stock_entry.get("items"):
            if item.get("is_finished_item") == 1:  # 1 for True in Frappe/ERPNext
                total_price += item.get("qty") * item.get("rate")

    return total_price



def get_average_production_time_per_product():
    total_duration = 0
    total_products = 0

    # Query Stock Entry records with purpose "Manufacture" and status "Submitted"
    stock_entries = frappe.get_all("Stock Entry",
        filters={"purpose": "Manufacture", "docstatus": 1}  # 1 for Submitted
    )

    for stock_entry in stock_entries:
        for item in stock_entry.get("items"):
            if item.get("is_finished_item") == 1:  # 1 for True in Frappe/ERPNext
                total_duration += (stock_entry.end_date - stock_entry.posting_date).days
                total_products += item.get("qty")

    average_time_per_product = total_duration / total_products if total_products > 0 else 0

    return average_time_per_product