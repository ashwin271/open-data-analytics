from data.working_data import working_data
from data.analytics_requests import analytics_requests
from modules.rule_parser import execute_rule
from modules.data_visualizer import data_visualizer

def main():
    analytics_results = []

    for analytics_request in analytics_requests:
        parsed_request = {**analytics_request}

        def replace_values(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    replace_values(value)
                elif key == "values" and isinstance(value, str) and '.' in value:
                    try:
                        parsed_value = execute_rule(working_data, value)
                    except ValueError as e:
                        print(f"Error processing rule '{value}': {e}")
                        parsed_value = []

                    # If parsed_value doesn't contain a function, access the field directly
                    if not parsed_value:
                        source_key, field_name = value.split('.', 1)
                        collection = working_data.get(source_key, [])
                        if collection is None:
                            print(f"Warning: No data found for source key '{source_key}'.")
                            parsed_value = []
                        else:
                            parsed_value = [item.get(field_name, None) for item in collection]
                    d[key] = parsed_value
        
        replace_values(parsed_request)
        analytics_results.append(parsed_request)

    print(analytics_results)
    print("---")

    # for analytics_result in analytics_results:
    #     print(analytics_result)
    #     data_visualizer(analytics_result)

if __name__ == "__main__":
    main()