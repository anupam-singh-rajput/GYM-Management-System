import frappe
from datetime import datetime

def execute(filters=None):
    data = frappe.db.sql("""
        SELECT
            YEAR(joining_date) AS year,
            MONTH(joining_date) AS month,
            SUM(final_price) AS total_revenue
        FROM `tabGYM Membership`
        WHERE joining_date IS NOT NULL
        AND docstatus < 2
        GROUP BY YEAR(joining_date), MONTH(joining_date)
        ORDER BY YEAR(joining_date), MONTH(joining_date)
    """, as_dict=True)

    # Format year and month into YYYY-MM string
    for row in data:
        row["month"] = f"{row['year']:04d}-{row['month']:02d}"
        # Remove the year and month keys, no longer needed
        row.pop("year")

    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 150},
        {"label": "Total Revenue ₹", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 200},
    ]

    chart = {
        "data": {
            "labels": [row["month"] for row in data],
            "datasets": [{
                "name": "Total Revenue",
                "values": [row["total_revenue"] for row in data]
            }]
        },
        "type": "bar",
        "colors": ["#36B37E"],
        "height": 300
    }

    return columns, data, None, chart
