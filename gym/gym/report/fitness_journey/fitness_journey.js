frappe.query_reports["Fitness Journey"] = {
  filters: [
    {
      fieldname: "member",
      label: "Gym Member",
      fieldtype: "Link",
      options: "BMI",
      reqd: 1
    }
  ]
};
