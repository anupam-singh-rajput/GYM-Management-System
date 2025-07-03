// Copyright (c) 2025, anupam and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Login", {
// 	refresh(frm) {

// 	},
// });
// frappe.ready(() => {
// if (frappe.web_form) {
// frappe.web_form.after_save = function () {
//         // Read data from the rendered fields
//         console.log("Hello World")
//         const email = $('[data-fieldname="email"] input').val();
//         const password = $('[data-fieldname="password"] input').val();
//         const role = $('[data-fieldname="role"] select').val();

//         console.log(email,password,role)

//         frappe.call({
//             method: "gym.api.login_user",  // Your app's backend method
//             args: {
//                 email: email,
//                 password: password,
//                 role: role
//             },
//             callback: function (r) {
//                 if (r.message) {
//                     frappe.msgprint(r.message);
//                     if (r.message === "Login successful") {
//                         console.log("User logged in.");
//                         // optional: window.location.href = "/dashboard";
//                     }
//                 }
//             }
//         });
//     }
// }
// });
