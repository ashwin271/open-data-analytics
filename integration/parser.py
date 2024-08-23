import re

# Dictionary of aggregate functions
AGGREGATE_FUNCTIONS = ['sum']

# Function registry to easily add new functions
FUNCTION_REGISTRY = {
    "sum": lambda data_list: sum(data_list),
    # Add more functions to the registry as needed
}

def apply_function(func_name, data_list):
    """Apply a registered function to the data list."""
    if func_name in FUNCTION_REGISTRY:
        return FUNCTION_REGISTRY[func_name](data_list)
    raise ValueError(f"Unsupported function: {func_name}")

def fetch_data(query, data):
    """Fetch data based on a query like 'category.field'."""
    if '.' not in query:
        raise ValueError(f"Invalid query format: '{query}'. Expected 'category.field'.")
    category, field = query.split('.')
    records = data.get(category, [])
    result = [record[field] for record in records if field in record]
    return result

def calculate_percentages(*data_lists):
    """Calculate percentages for the provided data lists."""
    total = sum(data_lists)
    if total == 0:
        return [0 for _ in data_lists]
    percentages = [(value / total) * 100 for value in data_lists]
    return percentages

def parse_expression(expression):
    """Parse the expression into individual tokens."""
    pattern = r'([a-zA-Z_][a-zA-Z0-9_\.]*)|(\w+\(.*?\))'
    tokens = re.findall(pattern, expression)
    return [t[0] if t[0] else t[1] for t in tokens]

def process_percentage_function(expression, data):
    """Handle the 'calculate_percentages' function specifically."""
    inner_expression = expression[len("calculate_percentages("):-1]
    data_lists = []
    sub_expressions = inner_expression.split(',')
    for sub_expr in sub_expressions:
        sub_expr = sub_expr.strip()
        func_match = re.match(r'(\w+)\((.*)\)', sub_expr)
        if func_match:
            func_name, arg = func_match.groups()
            data_list = fetch_data(arg, data)
            data_lists.append(apply_function(func_name, data_list))
        else:
            data_list = fetch_data(sub_expr, data)
            data_lists.append(data_list)
    return calculate_percentages(*data_lists)

def process_function(expression, data):
    """Process an expression that might include functions and data queries."""
    if "calculate_percentages(" in expression:
        return process_percentage_function(expression, data)

    tokens = parse_expression(expression)
    results = []
    
    for token in tokens:
        # Check if token is a function call
        func_match = re.match(r'(\w+)\((.*)\)', token)
        if func_match:
            func_name, arg = func_match.groups()
            data_list = fetch_data(arg, data)
            results.append(apply_function(func_name, data_list))
        elif token in FUNCTION_REGISTRY:
            # Token is a function name, which shouldn't be passed to fetch_data
            continue
        else:
            # Token is a data query
            results.extend(fetch_data(token, data))
    
    return results if len(results) > 1 else results[0]

def update_dict(a_dict, data):
    """Recursively update the dictionary with processed functions and data."""
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
