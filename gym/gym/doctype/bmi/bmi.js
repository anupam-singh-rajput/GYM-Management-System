// Copyright (c) 2025, anupam and contributors
// For license information, please see license.txt

// frappe.ui.form.on("BMI", {
// 	refresh(frm) {

// 	},
// });

// Copyright (c) 2025, anupam and contributors
// For license information, please see license.txt

// Copyright (c) 2025, anupam and contributors
// For license information, please see license.txt

frappe.ui.form.on('BMI', {
    // Trigger this when the form is loaded
    refresh(frm) {
        console.log("✅ BMI Form Loaded");

        // You can add any other refresh logic here
    },

    // Triggered when the 'table_qexv' (child table) is modified
    validate(frm) {
        // Add listeners for the blur event on the fields in the child table
        frm.fields_dict['table_qexv'].grid.get_field('height').$input.on('blur', function() {
            console.log("🔵 Height field modified");
            calculate_bmi(frm);
        });

        frm.fields_dict['table_qexv'].grid.get_field('weight').$input.on('blur', function() {
            console.log("🔵 Weight field modified");
            calculate_bmi(frm);
        });

        frm.fields_dict['table_qexv'].grid.get_field('calorie_intake').$input.on('blur', function() {
            console.log("🔵 Calorie Intake field modified");
            calculate_bmi(frm);
        });
    }
});

// Custom function to calculate BMI
function calculate_bmi(frm) {
    const rows = frm.doc.table_qexv || [];
    console.log("📝 Processing rows in table_qexv");

    rows.forEach(row => {
        const height = parseFloat(row.height);
        const weight = parseFloat(row.weight);
        const calorie = parseFloat(row.calorie_intake);

        console.log(`📝 Row: ${row.name}`);
        console.log("➡️ Height:", height);
        console.log("➡️ Weight:", weight);
        console.log("➡️ Calorie Intake:", calorie);

        if (!height || !weight || !calorie || height === 0) {
            console.log("⚠️ Missing or invalid input(s) for BMI calculation in row:", row.name);
            return;  // Skip this row if inputs are invalid
        }

        // Calculating BMI using the formula
        let bmi = (weight / (height * height)) + (calorie / 1000);
        bmi = bmi.toFixed(2); // Round to 2 decimal places

        console.log("✅ Calculated BMI (with calorie adjustment):", bmi);

        // Update the BMI field in the row
        frappe.model.set_value(row.doctype, row.name, 'bmi', bmi);
        console.log(`✅ BMI updated for row ${row.name}:`, bmi);
    });

    // Refresh the table to reflect updated values
    frm.refresh_field('table_qexv');
    console.log("✅ Table refreshed to show updated BMI values.");
}
