import re
from itertools import chain

# Dictionary of aggregate functions
AGGREGATE_FUNCTIONS = ['sum', 'calculate_percentages']

# Function registry to easily add new functions
FUNCTION_REGISTRY = {
    "sum": lambda data_list: add(flatten(data_list)),
    "calculate_percentages": lambda data_list: calculate_percentages(*data_list),
    # Add more functions to the registry as needed
}

def add(args):
    """Custom 'sum' function that sums all arguments as integers."""
    flattened_list = flatten(args)  # Flatten the entire list
    total = 0
    for item in flattened_list:
        total += int(item)  # Convert each item to an integer before summing
    return total

def flatten(lst):
    """Flatten a nested list structure."""
    if not isinstance(lst, list):
        return [lst]
    return list(chain.from_iterable(flatten(x) for x in lst))

def process_fn(func_name, arg_list):
    """Apply a registered function to the arg list."""
    if func_name in FUNCTION_REGISTRY:
        return FUNCTION_REGISTRY[func_name](arg_list)
    raise ValueError(f"Unsupported function: {func_name}")

def fetch_data(query, data):
    """Fetch data based on a query like 'category.field'."""
    if '.' not in query:
        raise ValueError(f"Invalid query format: '{query}'. Expected 'category.field'.")
    category, field = query.split('.')
    records = data.get(category, [])
    result = [record[field] for record in records if field in record]
    result = [int(x) for x in result]
    return result

def calculate_percentages(*args):
    # Ensure all arguments are lists
    args = [arg if isinstance(arg, list) else [arg] for arg in args]
    flattened_lists = [item for sublist in args for item in sublist]
    total = sum(flattened_lists)
    
    if total == 0:
        return [0 for _ in flattened_lists]  # Handle division by zero
    
    return [(item / total) * 100 for item in flattened_lists]

def fn_split(exp):
    """Split a function expression into function name and arguments."""
    match = re.match(r'(\w+)\((.*)\)', exp)
    if match:
        return match.group(1), match.group(2)
    return None, None

def parse_rule(exp, data):
    """Parse a rule or function call and return the result."""
    # Check if exp is just a rule or contains a function call
    func_name, args = fn_split(exp)
    
    if func_name is None:
        # It's just a rule
        return fetch_data(exp, data)
    else:
        # It contains a function call
        arg_list = [arg.strip() for arg in args.split(',')]
        processed_args = []
        for arg in arg_list:
            processed_arg = parse_rule(arg, data)
            processed_args.append(processed_arg)
        return process_fn(func_name, processed_args)

def update_dict(a_dict, data):
    """Recursively update the dictionary with processed rules and data."""
    for key, value in a_dict.items():
        if isinstance(value, dict):
            update_dict(value, data)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], dict):
                    update_dict(value[i], data)
                elif isinstance(value[i], str) and ("." in value[i] or any(func in value[i] for func in AGGREGATE_FUNCTIONS)):
                    a_dict[key][i] = parse_rule(value[i], data)
        elif isinstance(value, str) and ("." in value or any(func in value for func in AGGREGATE_FUNCTIONS)):
            a_dict[key] = parse_rule(value, data)