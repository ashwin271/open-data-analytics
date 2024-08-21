analytics_requests = [
    {
    "title": "Monthly Salary Expenses",
    "type": "bar",
    "axes": {
        "x_label": "Month",
        "y_label": "Salaries"
    },
    "data": {
        "x": ["July", "August", "September"],
        "y": {
            "label": "Monthly Salaries",
            "values": "monthly_expenses.salaries"
        }
    }
},
{
    "title": "Monthly Expenses Distribution",
    "type": "boxplot",
    "axes": {
        "x_label": "Expense Category",
        "x_values": ["Rent", "Utilities", "Salaries", "Marketing"],
        "y_label": "Cost"
    },
    "data": {
        "Rent": "monthly_expenses.rent",
        "Utilities": "monthly_expenses.utilities",
        "Salaries": "monthly_expenses.salaries",
        "Marketing": "monthly_expenses.marketing"
    }
},
    {
        "title": "Feedback Distribution",
        "type": "pie",
        "data": {
            "labels": {
                "values": "customer_feedback.date"
            },
            "percentages": {
                "values": "map(customer_feedback.positive_feedback, feedback -> feedback * 1.0)"
            }
        }
    },
    {
        "title": "Daily Food Sales Trends",
        "type": "line",
        "axes": {
            "x": {
                "label": "Date"
            },
            "y": {
                "label": "Food Sales"
            }
        },
        "x_values": {
            "values": "daily_operations.date"
        },
        "data": [
            {
                "label": "Food Sales Over Time",
                "y_values": {
                    "values": "daily_operations.food_sales"
                }
            }
        ]
    },
    {
        "title": "Beverage vs Dessert Sales",
        "type": "scatter",
        "axes": {
            "x": {
                "label": "Beverage Sales"
            },
            "y": {
                "label": "Dessert Sales"
            }
        },
        "data": [
            {
                "label": "Sales Correlation",
                "x_points": {
                    "values": "daily_operations.beverage_sales"
                },
                "y_points": {
                    "values": "daily_operations.dessert_sales"
                }
            }
        ]
    },
    {
        "title": "Distribution of Ingredient Costs",
        "type": "histogram",
        "axes": {
            "x": {
                "label": "Cost"
            },
            "y": {
                "label": "Frequency"
            }
        },
        "data": {
            "values": "inventory_management.ingredients_cost"
        }
    },
    {
        "title": "Monthly Expenses Distribution",
        "type": "boxplot",
        "axes": {
            "x": {
                "label": "Expense Category",
                "values": ["Rent", "Utilities", "Salaries", "Marketing"]
            },
            "y": {
                "label": "Cost"
            }
        },
        "data": {
            "rent": {
                "values": "monthly_expenses.rent"
            },
            "utilities": {
                "values": "monthly_expenses.utilities"
            },
            "salaries": {
                "values": "monthly_expenses.salaries"
            },
            "marketing": {
                "values": "monthly_expenses.marketing"
            }
        }
    }
]
