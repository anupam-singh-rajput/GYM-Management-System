// Copyright (c) 2025, anupam and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GYM Membership", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Gym Membership', {
book_locker: function (frm) {
// Show/hide the locker field based on the checkbox
frm.toggle_display('locker', frm.doc.book_locker === 1);

// Clear locker value if checkbox is unchecked
if (!frm.doc.book_locker) {
frm.set_value('locker', '');
}
},

onload: async function (frm) {
// Always ensure locker visibility is in sync
frm.toggle_display('locker', frm.doc.book_locker === 1);

// Fetch lockers that are already booked
const used_lockers = await frappe.db.get_list('Gym Membership', {
fields: ['locker'],
filters: {
docstatus: ['<', 2],
locker: ['!=', null]
},
pluck: 'locker'
});

// Set dynamic filter to exclude already-booked lockers
frm.set_query('locker', () => {
return {
filters: [
['Available Lockers', 'name', 'not in', used_lockers]
]
};
});
}
});