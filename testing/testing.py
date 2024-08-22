from main import process_and_visualize
from test_dataset import test_data
from test_analytics_template import test_analytics
import os

def run_test():
    results = []

    # Iterate through each database in the test datasets
    for db_name, db_data in test_data.items():
        analytics_templates = test_analytics.get(db_name, [])
        output_folder = f'test_visualizations/{db_name}'

        # Process and visualize the test analytics templates with test data
        try:
            processed_analytics = process_and_visualize(analytics_templates, db_data, output_folder)
            results.append((db_name, "Success"))
        except Exception as e:
            results.append((db_name, f"Failed: {str(e)}"))

    # Print the summary of test results
    for db_name, status in results:
        print(f"Database {db_name}: {status}")

if __name__ == "__main__":
    run_test()
