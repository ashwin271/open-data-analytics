import re
import copy
from typing import List, Dict, Any, Callable

# Dictionary of aggregate functions
AGGREGATE_FUNCTIONS: List[str] = ['sum']

# Function registry to easily add new functions
FUNCTION_REGISTRY: Dict[str, Callable[[List[Any]], Any]] = {}

def register_function(name: str, func: Callable[[List[Any]], Any]) -> None:
    """Register a new function in the FUNCTION_REGISTRY."""
    if not callable(func):
        raise ValueError("Function must be callable.")
    FUNCTION_REGISTRY[name] = func

# Registering the sum function
register_function("sum", lambda data_list: sum(data_list))

def apply_function(func_name: str, data_list: List[Any]) -> Any:
    """Apply a registered function to the data list."""
    if func_name in FUNCTION_REGISTRY:
        try:
            return FUNCTION_REGISTRY[func_name](data_list)
        except Exception as e:
            raise ValueError(f"Error applying function '{func_name}': {e}")
    raise ValueError(f"Unsupported function: {func_name}")

def fetch_data(query: str, data: Dict[str, List[Dict[str, Any]]]) -> List[Any]:
    """Fetch data based on a query like 'category.field'."""
    if '.' not in query:
        raise ValueError(f"Invalid query format: '{query}'. Expected 'category.field'.")
    category, field = query.split('.')
    if category not in data:
        raise ValueError(f"Category '{category}' not found in data.")
    records = data.get(category, [])
    result = [record[field] for record in records if field in record]
    if not result:
        raise ValueError(f"Field '{field}' not found in any record of category '{category}'.")
    return result

def calculate_percentages(*data_lists: List[float]) -> List[float]:
    """Calculate percentages for the provided data lists."""
    total = sum(data_lists)
    if total == 0:
        return [0 for _ in data_lists]
    percentages = [(value / total) * 100 for value in data_lists]
    return percentages

def parse_expression(expression: str) -> List[str]:
    """Parse the expression into individual tokens."""
    if len(expression) > 1000:  # Arbitrary limit to prevent ReDoS
        raise ValueError("Expression too long.")
    pattern = r'([a-zA-Z_][a-zA-Z0-9_\.]*)|(\w+\([^()]*\))'
    tokens = re.findall(pattern, expression)
    return [t[0] if t[0] else t[1] for t in tokens]

def process_percentage_function(expression: str, data: Dict[str, List[Dict[str, Any]]]) -> List[float]:
    """Handle the 'calculate_percentages' function specifically."""
    inner_expression = expression[len("calculate_percentages("):-1]
    data_lists = []
    sub_expressions = inner_expression.split(',')
    for sub_expr in sub_expressions:
        sub_expr = sub_expr.strip()
        func_match = re.match(r'(\w+)\((.*)\)', sub_expr)
        if func_match:
            func_name, arg = func_match.groups()
            if func_name not in FUNCTION_REGISTRY:
                raise ValueError(f"Unsupported function: {func_name}")
            data_list = fetch_data(arg, data)
            data_lists.append(apply_function(func_name, data_list))
        else:
            data_list = fetch_data(sub_expr, data)
            data_lists.append(data_list)
    return calculate_percentages(*data_lists)

def process_function(expression: str, data: Dict[str, List[Dict[str, Any]]]) -> Any:
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
            if func_name not in FUNCTION_REGISTRY:
                raise ValueError(f"Unsupported function: {func_name}")
            data_list = fetch_data(arg, data)
            results.append(apply_function(func_name, data_list))
        elif token in FUNCTION_REGISTRY:
            # Token is a function name, which shouldn't be passed to fetch_data
            continue
        else:
            # Token is a data query
            results.extend(fetch_data(token, data))
    
    return results if len(results) > 1 else results[0]

def update_dict(a_dict: Dict[str, Any], data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Recursively update the dictionary with processed functions and data."""
    a_dict = copy.deepcopy(a_dict)  # Create a deep copy to avoid side effects
    stack = [(a_dict, data)]
    while stack:
        current_dict, current_data = stack.pop()
        for key, value in current_dict.items():
            if isinstance(value, dict):
                stack.append((value, current_data))
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        stack.append((value[i], current_data))
                    elif isinstance(value[i], str) and ("." in value[i] or "calculate_percentages(" in value[i]):
                        current_dict[key][i] = process_function(value[i], current_data)
            elif isinstance(value, str) and ("." in value or "calculate_percentages(" in value):
                current_dict[key] = process_function(value, current_data)
    return a_dict