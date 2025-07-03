import frappe
from frappe import _

@frappe.whitelist()
def get_locker_settings():
    # Assuming only one LockerSetting record exists
    settings = frappe.get_all('LockerSetting', limit=1)
    if not settings:
        frappe.throw(_("LockerSetting not found"))

    doc = frappe.get_doc('LockerSetting', settings[0].name)
    return {
        'total_locker': doc.total_locker,
        'available_locker': doc.available_locker,
        'name': doc.name
    }

@frappe.whitelist()
def update_available_lockers(lockers_to_book: int):
    settings = frappe.get_all('LockerSetting', limit=1)
    if not settings:
        frappe.throw(_("LockerSetting not found"))

    doc = frappe.get_doc('LockerSetting', settings[0].name)

    if lockers_to_book > doc.available_locker:
        frappe.throw(_("Insufficient lockers available"))

    doc.available_locker -= lockers_to_book
    doc.save()
    frappe.db.commit()

    return {
        'available_locker': doc.available_locker
    }


import json
@frappe.whitelist()
# def get_filtered_trainers(doctype, txt, searchfield, start, page_len, filters=None):
#     if filters and isinstance(filters, str):
#         filters = json.loads(filters)
#     elif not filters:
#         filters = {}

#     specialization = filters.get('specialization')
#     conditions = []
#     values = []

#     if specialization:
#         conditions.append("specialization = %s")
#         values.append(specialization)

#     # Basic search condition on the searchfield (usually 'name' or 'name1')
#     query = f"""
#         SELECT name, name1 FROM `tabTrainerResgistration`
#         WHERE {searchfield} LIKE %s
#     """

#     values = [f"%{txt}%"] + values

#     if conditions:
#         query += " AND " + " AND ".join(conditions)

#     query += " LIMIT %s OFFSET %s"
#     values += [page_len, start]

#     results = frappe.db.sql(query, values, as_dict=True)
#     return results
@frappe.whitelist()
def get_filtered_trainers(doctype, txt, searchfield, start, page_len, filters=None):
    import json

    if filters and isinstance(filters, str):
        filters = json.loads(filters)
    elif not filters:
        filters = {}

    specialization = filters.get('specialization')
    conditions = []
    values = []

    if specialization:
        conditions.append("specialization = %s")
        values.append(specialization)

    start = int(start)
    page_len = int(page_len)

    query = f"""
        SELECT name, name1 FROM `tabTrainerResgistration`
        WHERE {searchfield} LIKE %s
    """

    values = [f"%{txt}%"] + values

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " LIMIT %s OFFSET %s"
    values += [page_len, start]

    results = frappe.db.sql(query, values, as_dict=True)

    # Map results to value-label format for dropdown
    mapped_results = [{"value": r["name"], "label": r["name1"]} for r in results]

    return mapped_results
