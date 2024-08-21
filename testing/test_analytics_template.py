# test_analytics_template.py

test_analytics = [
    {
        "title": "Test Sales Data",
        "type": "bar",
        "data": {
            "x": ["apple", "banana", "orange"],
            "y": [
                {
                    "label": "Quantity Sold",
                    "values": "sum(sales.quantity)"
                }
            ]
        },
        "axes": {
            "x_label": "Item",
            "y_label": "Total Quantity"
        }
    },
    {
        "title": "Test Expenses Breakdown",
        "type": "pie",
        "data": {
            "labels": ["rent", "salaries", "utilities"],
            "percentages": "calculate_percentages(sum(expenses.amount), sum(expenses.amount), sum(expenses.amount))"
        }
    }
]
