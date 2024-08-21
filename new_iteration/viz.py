import matplotlib.pyplot as plt

def create_plot(plot_data):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    if 'data' in plot_data:
        x_key = 'data'
    else:
        for k in plot_data:
            if k != 'axes' and k != 'title' and k != 'type':
                x_key = k
                break
    
    # Corrected indentation
    x = plot_data[x_key]['x']
    for y_data in plot_data[x_key]['y']:
        if plot_data['type'] == 'bar':
            ax.bar(x, y_data['values'], label=y_data['label'])
        elif plot_data['type'] == 'line':
            ax.plot(x, y_data['values'], label=y_data['label'])
        # Add more types as needed

    ax.set_title(plot_data['title'])
    ax.set_xlabel(plot_data['axes']['x_label'])
    ax.set_ylabel(plot_data['axes']['y_label'])
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
data2 = {
    'axes': {'x_label': 'Date', 'y_label': 'Sales Amount'},
    'data': {
        'x': [
            '2024-08-01',
            '2024-08-02',
            '2024-08-03',
            '2024-08-04',
            '2024-08-05'
        ],
        'y': [
            {'label': 'Food Sales', 'values': [1500, 1600, 1700, 1400, 1550]},
            {'label': 'Beverage Sales', 'values': [600, 700, 750, 650, 620]},
            {'label': 'Dessert Sales', 'values': [400, 420, 430, 415, 405]}
        ]
    },
    'title': 'Daily Sales Trends',
    'type': 'line'
}

create_plot(data2)
