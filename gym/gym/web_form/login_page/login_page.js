frappe.ready(function() {
    // Create the custom button
    let button = document.createElement('button');
    button.innerHTML = 'Log Form Data';
    button.type = 'button';
    button.className = 'btn btn-primary';
    button.style.marginTop = '10px';

    // Append the button to the Web Form footer
    const target = document.querySelector('.web-form-footer');
    if (target) {
        target.appendChild(button);
    }

    // Use Frappe's web_form object to get field values
    button.addEventListener('click', function() {
        const email = frappe.web_form.get_value('email');
        const role = frappe.web_form.get_value('role');
        const password = frappe.web_form.get_value('password');

        console.log('Email:', email);
        console.log('Role:', role);
        console.log('Password:', password);
    });
});
