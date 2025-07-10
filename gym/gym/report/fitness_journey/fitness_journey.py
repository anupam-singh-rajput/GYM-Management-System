import frappe

def execute(filters=None):
    filters = filters or {}
    member = filters.get("member")
    if not member or not isinstance(member, str):
        frappe.throw("Please select a valid member.")

    data = frappe.db.sql("""
        SELECT
            m.date,
            m.weight AS current_weight,
            m.height AS current_height,
            m.calorie_intake AS daily_calorie_intake,
            m.bmi
        FROM
            `tabBMI` b
            JOIN `tabMetrics Update` m ON m.parent = b.name
        WHERE
            b.name = %s
        ORDER BY
            m.date ASC
    """, (member,), as_dict=True)

    if not data:
        frappe.msgprint("No fitness data found for this member.")

    labels = []
    weights = []
    calories = []
    bmis = []

    for d in data:
        date_str = d.get("date").strftime("%Y-%m-%d") if d.get("date") else ""
        labels.append(date_str)
        weights.append(d.get("current_weight") or 0)
        calories.append(d.get("daily_calorie_intake") or 0)
        bmis.append(d.get("bmi") or 0)

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Weight (kg)", "fieldname": "current_weight", "fieldtype": "Float", "width": 120},
        {"label": "Height (cm)", "fieldname": "current_height", "fieldtype": "Float", "width": 120},
        {"label": "Daily Calories", "fieldname": "daily_calorie_intake", "fieldtype": "Int", "width": 140},
        {"label": "BMI", "fieldname": "bmi", "fieldtype": "Float", "width": 100},
    ]

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Weight (kg)", "values": weights},
                {"name": "Calories", "values": calories},
                {"name": "BMI", "values": bmis},
            ],
        },
        "type": "line",
        "colors": ["#36a2eb", "#ff6384", "#4caf50"],
    }

    return columns, data, None, chart
