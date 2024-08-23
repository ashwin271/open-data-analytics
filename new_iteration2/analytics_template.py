analytics = [
    {
        "title": "Monthly Salary and Bonus Expenses",
        "type": "bar",
        "axes": {
            "x_label": "Month",
            "y_label": "Amount"
        },
        "data": {
            "x": ["July", "August", "September"],
            "y": [
                {
                    "label": "Salaries",
                    "values": "monthly_expenses.salaries"
                },
                {
                    "label": "Bonuses",
                    "values": "monthly_expenses.rent"  # Replace with actual bonus data path if applicable
                },
                {
                    "label": "Utils",
                    "values": "monthly_expenses.utilities" 
                },
                {
                    "label": "Marketing",
                    "values": "monthly_expenses.marketing" 
                }
            ]
        }
    },
    {
        "title": "Daily Sales Trends",
        "type": "line",
        "axes": {
            "x_label": "Date",
            "y_label": "Sales Amount"
        },
        "data": {
            "x": "daily_operations.date",
            "y": [
                {
                    "label": "Food Sales",
                    "values": "daily_operations.food_sales"
                },
                {
                    "label": "Beverage Sales",
                    "values": "daily_operations.beverage_sales"
                },
                {
                    "label": "Dessert Sales",
                    "values": "daily_operations.dessert_sales"
                }
            ]
        }
    },
    {
        "title": "Beverage vs Dessert Sales",
        "type": "scatter",
        "axes": {
            "x_label": "Beverage Sales",
            "y_label": "Sales Amount"
        },
        "data": {
            "x": "daily_operations.beverage_sales",
            "y": [
                {
                    "label": "Dessert Sales",
                    "values": "daily_operations.dessert_sales"
                },
                {
                    "label": "Food Sales",
                    "values": "daily_operations.food_sales"
                }
            ]
        }
    },
    {
        "title": "Customer Feedback Distribution",
        "type": "pie",
        "data": {
            "labels": ["Positive", "Negative"],
            "percentages": "calculate_percentages(sum(customer_feedback.positive_feedback),sum(customer_feedback.negative_feedback))"
        }
    }
]
