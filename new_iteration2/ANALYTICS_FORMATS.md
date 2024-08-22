# Analytics Template Guide

This document explains how to write analytics templates for visualizing data. Each template includes details on the type of chart, axes labels, and data specifications.

## Analytics Template Format

Each analytics template is a dictionary that includes the following keys:

- `title`: The title of the chart.
- `type`: The type of chart (e.g., "bar", "line", "scatter", "pie").
- `axes` (optional): Labels for the x and y axes (for bar, line, and scatter charts).
- `data`: The data used to generate the chart. This can include labels, values, and how to calculate percentages.

## Example Templates

### Bar Chart

**Title:** Monthly Salary and Bonus Expenses

```python
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
            }
        ]
    }
}
```

**Description:**

- `type`: "bar" - Specifies that this is a bar chart.
- `axes`: Provides labels for the x-axis and y-axis.
- `data`: 
  - `x`: A list of categories (months).
  - `y`: A list of series with labels and data paths for the y-axis values.

### Line Graph

**Title:** Daily Sales Trends

```python
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
}
```

**Description:**

- `type`: "line" - Specifies that this is a line graph.
- `axes`: Provides labels for the x-axis (date) and y-axis (sales amount).
- `data`: 
  - `x`: Data path for the x-axis values (dates).
  - `y`: A list of series with labels and data paths for the y-axis values.

### Scatter Plot

**Title:** Beverage vs Dessert Sales

```python
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
}
```

**Description:**

- `type`: "scatter" - Specifies that this is a scatter plot.
- `axes`: Provides labels for the x-axis (beverage sales) and y-axis (sales amount).
- `data`: 
  - `x`: Data path for the x-axis values (beverage sales).
  - `y`: A list of series with labels and data paths for the y-axis values.

### Pie Chart

**Title:** Customer Feedback Distribution

```python
{
    "title": "Customer Feedback Distribution",
    "type": "pie",
    "data": {
        "labels": ["Positive", "Negative"],
        "percentages": "calculate_percentages(sum(customer_feedback.positive_feedback), sum(customer_feedback.negative_feedback))"
    }
}
```

**Description:**

- `type`: "pie" - Specifies that this is a pie chart.
- `data`: 
  - `labels`: List of categories (positive, negative).
  - `percentages`: A formula to calculate the percentages based on feedback data.

## Tips for Writing Templates

- Ensure `values` points to the correct data path in your dataset.
- For pie charts, use functions like `calculate_percentages` to process data.
- Customize the `axes` labels and `data` structure based on the type of chart and the data you have.

Feel free to adapt these templates to fit your specific data and visualization needs.