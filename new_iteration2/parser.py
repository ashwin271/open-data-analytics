import re

# Dictionary of aggregate functions
AGGREGATE_FUNCTIONS = ['sum']

def aggregate_function(func_name, data_list):
    if func_name == "sum":
        return sum(data_list)
    # Add more aggregate functions here
    raise ValueError(f"Unknown aggregate function: {func_name}")

def fetch_data(query, data):
    category, field = query.split('.')
    records = data.get(category, [])
    result = [record[field] for record in records if field in record]
    return result

def calculate_percentages(*data_lists):
    total = sum(data_lists)
    if total == 0:
        return [0 for _ in data_lists]
    percentages = [(value / total) * 100 for value in data_lists]
    return percentages

def parse_expression(expression):
    pattern = r'([a-zA-Z_][a-zA-Z0-9_\.]*)|(\w+\(.*?\))'
    tokens = re.findall(pattern, expression)
    return [t[0] if t[0] else t[1] for t in tokens]

def process_function(expression, data):
    if "calculate_percentages(" in expression:
        inner_expression = expression[len("calculate_percentages("):-1]
        data_lists = []
        sub_expressions = inner_expression.split(',')
        for sub_expr in sub_expressions:
            sub_expr = sub_expr.strip()
            func_match = re.match(r'(\w+)\((.*)\)', sub_expr)
            if func_match:
                func_name, arg = func_match.groups()
                if func_name in AGGREGATE_FUNCTIONS:
                    data_list = fetch_data(arg, data)
                    aggregated_value = aggregate_function(func_name, data_list)
                    data_lists.append(aggregated_value)
                else:
                    raise ValueError(f"Unsupported function: {func_name}")
            else:
                data_list = fetch_data(sub_expr, data)
                data_lists.append(data_list)
        return calculate_percentages(*data_lists)

    tokens = parse_expression(expression)
    if len(tokens) == 1:
        return fetch_data(tokens[0], data)

    aggregated_data = []
    for token in tokens:
        func_match = re.match(r'(\w+)\((.*)\)', token)
        if func_match:
            func_name, arg = func_match.groups()
            if func_name in AGGREGATE_FUNCTIONS:
                data_list = fetch_data(arg, data)
                aggregated_value = aggregate_function(func_name, data_list)
                aggregated_data.append(aggregated_value)
            else:
                raise ValueError(f"Unsupported function: {func_name}")
        else:
            data_list = fetch_data(token, data)
            aggregated_data.append(data_list)

    return aggregated_data

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
