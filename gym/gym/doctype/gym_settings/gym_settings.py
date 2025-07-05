# Copyright (c) 2025, anupam and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class GymSettings(Document):
	
    def validate(self):
        self.set_locker_description()

    def set_locker_description(self):
        count = int(self.locker or 0)
        if count > 0:
            import random
            locks = [f"L{random.randint(100,999)}" for _ in range(count)]
            self.locker_description = "Assigned Lockers: " + ", ".join(locks)
        else:
            self.locker_description = ""
