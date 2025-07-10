import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Class (Category)",
            "fieldname": "class_booking",
            "fieldtype": "Link",
            "options": "Categories",  # Fix: should match the Link in JSON
            "width": 250
        },
        {
            "label": "Total Bookings",
            "fieldname": "total",
            "fieldtype": "Int",
            "width": 150
        }
    ]

    data = frappe.db.sql("""
        SELECT
            class_boooking AS class_booking,
            COUNT(*) AS total
        FROM `tabGym Class Booking`
        WHERE class_boooking IS NOT NULL
        AND docstatus < 2
        GROUP BY class_boooking
        ORDER BY total DESC
    """, as_dict=True)

    chart = {
        "data": {
            "labels": [row["class_booking"] for row in data],
            "datasets": [
                {
                    "name": "Total Bookings",
                    "values": [row["total"] for row in data]
                }
            ]
        },
        "type": "bar",
        "colors": ["#FFA500"]
    }

    return columns, data, None, chart
