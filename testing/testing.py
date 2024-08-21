# testing.py

from main import process_and_visualize
from test_dataset import test_data
from test_analytics_template import test_analytics
from pprint import pprint
import os

def run_test():
    # Define a separate output folder for test visualizations
    test_output_folder = 'test_visualizations'

    # Process and visualize the test analytics templates with test data
    processed_analytics = process_and_visualize(test_analytics, test_data, test_output_folder)

    # Print the updated test analytics templates
    for template in processed_analytics:
        pprint(template)

if __name__ == "__main__":
    # Ensure that the test output folder exists
    if not os.path.exists('test_visualizations'):
        os.makedirs('test_visualizations')
    
    run_test()
