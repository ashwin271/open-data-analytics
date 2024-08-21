from parser import update_dict
from viz import create_plot
from pprint import pprint
import matplotlib.pyplot as plt
import os

def process_and_visualize(analytics_list, dataset, output_folder='visualizations'):
    processed_analytics = []

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Step 1: Process each analytics dictionary
    for template in analytics_list:
        update_dict(template, dataset)
        processed_analytics.append(template)
    
    # Step 2: Visualize and save each processed analytics dictionary
    for i, template in enumerate(processed_analytics):
        # Create plot
        create_plot(template)
        # Save the figure
        plt.savefig(f"{output_folder}/plot_{i + 1}.png")
        plt.close()

    return processed_analytics

def main():
    from analytics_template import analytics
    from dataset import data
    # Process and visualize the analytics templates with actual data
    output_folder = 'visualizations'
    processed_analytics = process_and_visualize(analytics, data, output_folder)

    # Print or process the updated analytics templates
    for template in processed_analytics:
        pprint(template)

if __name__ == "__main__":

    main()
