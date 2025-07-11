import frappe
from frappe.utils import nowdate, getdate

@frappe.whitelist()
def get_member_details():
    user_email = frappe.session.user

    # Step 1: Get Gym Member Name using email
    gym_member_name = frappe.get_value("Gym Members", {"email": user_email}, "name")
    if not gym_member_name:
        return {}

    # Step 2: Get Membership details using Gym Member name
    membership = frappe.get_all(
        'GYM Membership',
        filters={'email': gym_member_name},  # Changed email_id to email
        limit=1,
        order_by='creation desc',
        fields=['email', 'contact', 'plans', 'joining_date', 'ending_date']  # Changed email_id to email
    )

    if not membership:
        return {}

    member = membership[0]

    # Step 3: Calculate remaining days
    remaining_days = None
    if member.get('ending_date'):
        remaining_days = (getdate(member['ending_date']) - getdate(nowdate())).days

    # Step 4: Get Trainer Name from Gym Class Booking
    booking = frappe.get_all(
        'Gym Class Booking',
        filters={'email': user_email},
        limit=1,
        order_by='creation desc',
        fields=['trainer_name']
    )

    trainer_name = booking[0]['trainer_name'] if booking else 'N/A'

    return {
        "email": user_email,
        "contact": member.get('contact'),
        "plan": member.get('plans'),
        "joining_date": member.get('joining_date'),
        "ending_date": member.get('ending_date'),
        "remaining_days": remaining_days,
        "trainer": {
            "name": trainer_name
        }
    }
