working_data = {
    "daily_operations": [
        {"date": "2024-08-01", "food_sales": 1500, "beverage_sales": 600, "dessert_sales": 400, "appetizer_sales": 300},
        {"date": "2024-08-02", "food_sales": 1600, "beverage_sales": 700, "dessert_sales": 420, "appetizer_sales": 320},
        {"date": "2024-08-03", "food_sales": 1700, "beverage_sales": 750, "dessert_sales": 430, "appetizer_sales": 340},
        {"date": "2024-08-04", "food_sales": 1400, "beverage_sales": 650, "dessert_sales": 415, "appetizer_sales": 310},
        {"date": "2024-08-05", "food_sales": 1550, "beverage_sales": 620, "dessert_sales": 405, "appetizer_sales": 305}
    ],
    "monthly_expenses": [
        {"month": "2024-07", "rent": 2000, "utilities": 350, "salaries": 5000, "marketing": 800},
        {"month": "2024-08", "rent": 2000, "utilities": 360, "salaries": 5200, "marketing": 850},
        {"month": "2024-09", "rent": 2100, "utilities": 370, "salaries": 5300, "marketing": 900}
    ],
    "customer_feedback": [
        {"date": "2024-08-01", "positive_feedback": 50, "negative_feedback": 5},
        {"date": "2024-08-02", "positive_feedback": 60, "negative_feedback": 7},
        {"date": "2024-08-03", "positive_feedback": 70, "negative_feedback": 6},
        {"date": "2024-08-04", "positive_feedback": 55, "negative_feedback": 8},
        {"date": "2024-08-05", "positive_feedback": 65, "negative_feedback": 5}
    ],
    "inventory_management": [
        {"inventory_date": "2024-08-01", "ingredients_cost": 750, "beverages_cost": 150},
        {"inventory_date": "2024-08-02", "ingredients_cost": 780, "beverages_cost": 160},
        {"inventory_date": "2024-08-03", "ingredients_cost": 790, "beverages_cost": 170},
        {"inventory_date": "2024-08-04", "ingredients_cost": 760, "beverages_cost": 140},
        {"inventory_date": "2024-08-05", "ingredients_cost": 770, "beverages_cost": 155}
    ]
}

analytics_requests = [
    {
        "title": "Monthly Salary Expenses",
        "type": "bar",
        "axes": {
            "x": {
                "label": "Month"
            },
            "y": {
                "label": "Salaries"
            }
        },
        "x_values": {
            "values": ["July", "August", "September"]
        },
        "data": [
            {
                "label": "Monthly Salaries",
                "y_values": {
                    "values": "monthly_expenses.salaries"
                }
            }
        ]
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

analytics_results = []

for analytics_request in analytics_requests:

    # for all keys with name "value" and its pair not being an array ( includes nested dicts ) in analytics_request
    # run the rule parser with the string extracted from the key and the working_data passed into it
    # substitute the value pair with what was returned by the rule parser , which is an array
    # append the modified request to analytics_results

    analytics_results.append(analytics_request)


for analytics_result in analytics_results:
    data_visualizer(analytics_result)