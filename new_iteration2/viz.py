import matplotlib.pyplot as plt
import numpy as np

def create_plot(plot_data):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    plot_type = plot_data.get('type')

    if plot_type in ['bar', 'line', 'scatter']:
        x = plot_data['data']['x']
        y_data = plot_data['data']['y']
        x_indexes = np.arange(len(x))

        if plot_type == 'bar':
            bar_width = 0.2
            for i, y in enumerate(y_data):
                offset = i * bar_width
                ax.bar(x_indexes + offset, y['values'], width=bar_width, label=y['label'])
            ax.set_xticks(x_indexes + bar_width * (len(y_data) - 1) / 2)
            ax.set_xticklabels(x)
        elif plot_type == 'line':
            for y in y_data:
                ax.plot(x, y['values'], label=y['label'], marker='o')
        elif plot_type == 'scatter':
            for y in y_data:
                ax.scatter(x, y['values'], label=y['label'])

    elif plot_type == 'pie':
        labels = plot_data['data']['labels']
        percentages = plot_data['data']['percentages']
        ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle

    ax.set_title(plot_data['title'])

    if plot_type in ['bar', 'line', 'scatter']:
        ax.set_xlabel(plot_data['axes']['x_label'])
        ax.set_ylabel(plot_data['axes']['y_label'])
        ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

# Example dataset to be visualized
examples = [
    {
        'title': 'Monthly Salary and Bonus Expenses',
        'type': 'bar',
        'axes': {'x_label': 'Month', 'y_label': 'Amount'},
        'data': {
            'x': ['July', 'August', 'September'],
            'y': [
                {'label': 'Salaries', 'values': [5000, 5200, 5300]},
                {'label': 'Bonuses', 'values': [2000, 2000, 2100]}
            ]
        }
    },
    {
        'title': 'Daily Sales Trends',
        'type': 'line',
        'axes': {'x_label': 'Date', 'y_label': 'Sales Amount'},
        'data': {
            'x': ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05'],
            'y': [
                {'label': 'Food Sales', 'values': [1500, 1600, 1700, 1400, 1550]},
                {'label': 'Beverage Sales', 'values': [600, 700, 750, 650, 620]},
                {'label': 'Dessert Sales', 'values': [400, 420, 430, 415, 405]}
            ]
        }
    },
    {
        'title': 'Beverage vs Dessert Sales',
        'type': 'scatter',
        'axes': {'x_label': 'Beverage Sales', 'y_label': 'Sales Amount'},
        'data': {
            'x': [600, 700, 750, 650, 620],
            'y': [
                {'label': 'Dessert Sales', 'values': [400, 420, 430, 415, 405]},
                {'label': 'Food Sales', 'values': [1500, 1600, 1700, 1400, 1550]}
            ]
        }
    },
    {
        'title': 'Customer Feedback Distribution',
        'type': 'pie',
        'data': {
            'labels': ['Positive', 'Negative'],
            'percentages': [90.63, 9.37]
        }
    }
]

# Creating the plots based on example data
for example in examples:
    create_plot(example)
