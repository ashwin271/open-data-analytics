import os
from viz import create_plot
import matplotlib.pyplot as plt

def test_visualizations(visualizations, output_folder="test"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for i, plot_data in enumerate(visualizations):
        # Generate the plot
        create_plot(plot_data)
        
        # Save the plot as an image in the output folder
        output_path = os.path.join(output_folder, f"plot_{i+1}.png")
        plt.savefig(output_path)
        plt.close()  # Close the plot to avoid memory issues

if __name__ == "__main__":
    # Example visualization objects
    visualizations = [
        {'axes': {'x_label': 'Stage', 'y_label': 'Total Inventory'},
  'data': {'x': ['Warehouse', 'Shop', 'Sales'],
           'y': [{'label': 'Warehouse',
                  'values': [200, 300, 400]},
                 {'label': 'Shop',
                  'values': [100, 150, 200]},
                 {'label': 'Sales',
                  'values': [10, 15, 5]}]},
  'title': 'Total Inventory Comparison',
  'type': 'bar'}
    ]
    
    # Run the test
    test_visualizations(visualizations)