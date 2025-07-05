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


#--------------------------------------------------------------------------------------------
import frappe
from frappe import _


@frappe.whitelist()
def get_membership_report(member_id):
    try:
        if not member_id:
            return None

        # 🔍 Try direct lookup by name (ID)
        if frappe.db.exists("GYM Membership", member_id):
            membership = frappe.get_doc("GYM Membership", member_id)
        else:
            # 🔁 Fallback: search by member name
            result = frappe.get_all(
                "GYM Membership",
                filters={"name1": ["like", f"%{member_id}%"]},
                fields=["name"],
                limit=1
            )
            if result:
                membership = frappe.get_doc("GYM Membership", result[0].name)
            else:
                return None

        # 🏷️ Specialization Label from linked Categories DocType
        specialization_label = ""
        if membership.specialization:
            try:
                spec_doc = frappe.get_doc("Categories", membership.specialization)
                specialization_label = (
                    spec_doc.get("specialization")
                    or spec_doc.get("category_name")
                    or spec_doc.get("title")
                    or spec_doc.get("name")
                    or membership.specialization
                )
                frappe.log_error("Specialization Debug", f"Fetched: {specialization_label}")
            except Exception as e:
                specialization_label = membership.specialization
                frappe.log_error("Specialization Fetch Error", str(e))

        # 🧑‍🏫 Trainer Name from linked Trainer DocType
        trainer_name = membership.get("trainer")
        if trainer_name:
            try:
                trainer_doc = frappe.get_doc("Trainer", trainer_name)
                trainer_name = (
                    trainer_doc.get("trainer_name")
                    or trainer_doc.get("full_name")
                    or trainer_doc.get("name")
                    or membership.get("trainer")
                )
                frappe.log_error("Trainer Debug", f"Fetched: {trainer_name}")
            except Exception as e:
                frappe.log_error("Trainer Fetch Error", str(e))

        # 📊 Fitness Tracking from child table
        fitness_track = []
        if membership.metrics_update:
            for row in membership.metrics_update:
                fitness_track.append({
                    "metric": getattr(row, "metric", ""),
                    "height": getattr(row, "height", ""),
                    "weight": getattr(row, "weight", ""),
                    "calories": getattr(row, "calorie_intake", ""),
                    "bmi": getattr(row, "bmi", "")
                })

        # ✅ Return final structured data
        return {
            "name1": membership.get("name1"),
            "contact": membership.get("contact"),
            "email_id": membership.get("email") or membership.get("email_id"),
            "gender": membership.get("gender"),
            "plans": membership.get("plans"),
            "joining_date": membership.get("joining_date"),
            "ending_date": membership.get("ending_date"),
            "assign_locker": membership.get("assign_locker"),
            "locker": membership.get("locker"),
            "address": membership.get("address"),
            "specialization": specialization_label,
            "trainer": trainer_name,
            "fitness_track": fitness_track
        }

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Customer Report API Error")
        frappe.throw(_("Something went wrong while generating the report."))
