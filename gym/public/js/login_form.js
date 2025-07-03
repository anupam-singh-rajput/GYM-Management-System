frappe.ready(function () {
    $(".btn-login").on("click", function () {
        // Read data from the rendered fields
        const email = $('[data-fieldname="email"] input').val();
        const password = $('[data-fieldname="password"] input').val();
        const role = $('[data-fieldname="role"] select').val();

        frappe.call({
            method: "gym.api.login_user",  // Your app's backend method
            args: {
                email: email,
                password: password,
                role: role
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                    if (r.message === "Login successful") {
                        console.log("User logged in.");
                        // optional: window.location.href = "/dashboard";
                    }
                }
            }
        });
    });
});
