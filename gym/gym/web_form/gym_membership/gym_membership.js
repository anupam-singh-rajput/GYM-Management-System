frappe.ready(async function () {
    console.log("✅ Gym WebForm JS Loaded");

    // 1. Fetch available lockers from backend and set field
    await frappe.call({
        method: "gym.gym.api.get_locker_settings",
        callback: function (r) {
            if (r.message) {
                let available = r.message.available_locker;
                frappe.web_form.set_value("available", available);
                frappe.web_form.available_lockers = available; // store for local comparison
                frappe.web_form.locker_setting_name = r.message.name;
            }
        }
    });

    // 2. Locker field on change handler
    frappe.web_form.on("locker", async function () {
        const locker_count = parseInt(frappe.web_form.get_value("locker") || "0");
        const available = parseInt(frappe.web_form.available_lockers || "0");

        // Validate number
        if (isNaN(locker_count) || locker_count <= 0) {
            frappe.msgprint("Please enter a valid locker count.");
            frappe.web_form.set_value("locker", "");
            return;
        }

        // Check if enough lockers are available
        if (locker_count > available) {
            frappe.msgprint("Insufficient lockers available.");
            frappe.web_form.set_value("locker", ""); // reset field
            return;
        }

        // 3. Proceed with booking lockers
        try {
            const r = await frappe.call({
                method: "gym.gym.api.update_available_lockers",
                args: {
                    lockers_to_book: locker_count
                }
            });

            if (r.message) {
                frappe.web_form.set_value("available", r.message.available_locker);
                frappe.web_form.available_lockers = r.message.available_locker; // update local cache
            }
        } catch (e) {
            console.error("Update failed", e);
            frappe.msgprint("Server error while updating lockers.");
        }
    });

    
});
