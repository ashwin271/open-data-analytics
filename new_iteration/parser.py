def fetch_data(query, data):
    category, field = query.split('.')
    records = data.get(category, [])
    result = [record[field] for record in records if field in record]
    return result

def calculate_percentages(*data_lists):
    total = sum([sum(data_list) for data_list in data_lists])
    percentages = [(sum(data_list) / total) * 100 for data_list in data_lists]
    return percentages

def process_function(expression, data):
    if expression.startswith("calculate_percentages(") and expression.endswith(")"):
        # Extract the data queries from the function call
        inner_expr = expression[len("calculate_percentages("):-1]
        queries = inner_expr.split(", ")
        
        # Fetch the data for each query
        data_lists = [fetch_data(query, data) for query in queries]
        
        # Calculate percentages
        return calculate_percentages(*data_lists)
    
    return fetch_data(expression, data)

def update_dict(a_dict, data):
    for key, value in a_dict.items():
        if isinstance(value, dict):
            update_dict(value, data)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], dict):
                    update_dict(value[i], data)
                elif isinstance(value[i], str) and ("." in value[i] or "calculate_percentages(" in value[i]):
                    a_dict[key][i] = process_function(value[i], data)
        elif isinstance(value, str) and ("." in value or "calculate_percentages(" in value):
            a_dict[key] = process_function(value, data)

