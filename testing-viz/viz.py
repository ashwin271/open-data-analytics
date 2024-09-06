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
    # plt.tight_layout()
    # plt.show()

