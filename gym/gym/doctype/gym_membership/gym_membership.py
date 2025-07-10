# Copyright (c) 2025, anupam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GYMMembership(Document):
	def set_locker_description(self):
		count = int(self.locker or 0)
		if count > 0:
			import random
			locks = [f"L{random.randint(100,999)}" for _ in range(count)]
			self.locker_description = "Assigned Lockers: " + ", ".join(locks)
		else:
			self.locker_description = ""

	# def validate(self):
    #     self.calculate_final_price()

    # def calculate_final_price(self):
	# 	settings = frappe.get_single("Gym Settings")

    #     plan_prices = {
    #         "1 Month (₹5000)": settings.default_price_1m,
    #         "3 Months (₹9000)": settings.default_price_3m,
    #         "1 Year (₹14000)": settings.default_price_1y
    #     }

    #     selected_plan = getattr(self, 'plans', '')

    #     base_price = plan_prices.get(selected_plan, 0)

    #     locker_price = 1500 if (self.assign_locker == "Yes") else 0

    #     self.final_price = base_price + locker_price