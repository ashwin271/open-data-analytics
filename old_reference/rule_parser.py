from typing import Callable, List, Dict, Any, Tuple, Union
import numpy as np

# Define types
OperationFunction = Callable[[List[float]], float]
TransformationFunction = Callable[[List[float]], List[float]]
MapFunction = Callable[[float], float]
FilterFunction = Callable[[Dict[str, Any]], bool]

# Registries for all operations
aggregation_functions: Dict[str, OperationFunction] = {}
transformation_functions: Dict[str, Union[TransformationFunction, Callable[..., List[float]]]] = {}

# Aggregation Functions
def agg_sum(array: List[float]) -> float:
    return sum(array)

def agg_avg(array: List[float]) -> float:
    return np.mean(array)

def agg_median(array: List[float]) -> float:
    return np.median(array)

def agg_stddev(array: List[float]) -> float:
    return np.std(array)

def agg_min(array: List[float]) -> float:
    return min(array)

def agg_max(array: List[float]) -> float:
    return max(array)

# Register Aggregation Functions
aggregation_functions.update({
    "sum": agg_sum,
    "avg": agg_avg,
    "median": agg_median,
    "stddev": agg_stddev,
    "min": agg_min,
    "max": agg_max,
})

# Transformation Functions
def transform_softmax(array: List[float]) -> List[float]:
    exp_values = np.exp(array - np.max(array))
    return (exp_values / np.sum(exp_values)).tolist()

def transform_log(array: List[float]) -> List[float]:
    return np.log(array).tolist()

def transform_cumsum(array: List[float]) -> List[float]:
    return np.cumsum(array).tolist()

def elementwise_add(array1: List[float], array2: List[float]) -> List[float]:
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length for elementwise addition.")
    return [x + y for x, y in zip(array1, array2)]

# Register Transformation Functions
transformation_functions.update({
    "softmax": transform_softmax,
    "log_transform": transform_log,
    "cumsum": transform_cumsum,
    "add_arrays": elementwise_add,
})

# Utility Functions
def parse_condition(condition: str) -> Tuple[str, str, float]:
    operators = ['>', '<', '==']
    for op in operators:
        if op in condition:
            field, value = condition.split(op)
            return field.strip(), op, float(value.strip())
    raise ValueError("Invalid condition format.")

def evaluate_condition(item_value: Any, operator: str, compare_value: Any) -> bool:
    if operator == '>':
        return item_value > compare_value
    elif operator == '<':
        return item_value < compare_value
    elif operator == '==':
        return item_value == compare_value
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def filter_data(collection: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
    field, op, value = parse_condition(condition)
    return [item for item in collection if evaluate_condition(item.get(field), op, value)]

def parse_rule(rule: str) -> Tuple[str, List[str]]:
    func_name, args_string = rule.split("(", 1)
    args_string = args_string.rstrip(")")
    return func_name.strip(), split_arguments(args_string)

def split_arguments(args_string: str) -> List[str]:
    args = []
    start = 0
    depth = 0
    for i, char in enumerate(args_string):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == ',' and depth == 0:
            args.append(args_string[start:i].strip())
            start = i + 1
    args.append(args_string[start:].strip())
    return args

def parse_field_identifier(identifier: str) -> Tuple[str, str]:
    try:
        collection_name, field_name = identifier.split('.', 1)
        return collection_name.strip(), field_name.strip()
    except ValueError:
        raise ValueError(f"Invalid field identifier: {identifier}")

# Rule Execution
def execute_rule(export_table: Dict[str, List[Dict[str, Any]]], rule: str) -> List[Any]:
    func_name, args = parse_rule(rule)

    if func_name in aggregation_functions:
        source_key, field_name = parse_field_identifier(args[0])
        field_values = [item.get(field_name, 0) for item in export_table.get(source_key, [])]
        return [aggregation_functions[func_name](field_values)]

    elif func_name in transformation_functions:
        if func_name == 'add_arrays':
            array1_values = execute_rule(export_table, args[0])
            array2_values = execute_rule(export_table, args[1])
            return transformation_functions[func_name](array1_values, array2_values)
        else:
            values = execute_rule(export_table, args[0])
            return transformation_functions[func_name](values)

    elif func_name == 'filter':
        source_key, condition = args
        collection = export_table.get(source_key, [])
        return filter_data(collection, condition)

    elif func_name == 'combine':
        combined_result = []
        for arg in args:
            combined_result.extend(execute_rule(export_table, arg))
        return combined_result

    elif func_name == 'map':
        collection_rule, map_expr = args
        collection = execute_rule(export_table, collection_rule)
        # Use eval carefully
        return [eval(map_expr.replace("x ->", "").strip(), {"x": x}) for x in collection]

    elif func_name == 'sort':
        source_key, sort_rule = args
        collection = export_table.get(source_key, [])
        field, order = sort_rule.split()
        reverse = order.lower() == 'desc'
        return sorted(collection, key=lambda x: x[field], reverse=reverse)

    elif '.' in rule:
        source_key, field_name = parse_field_identifier(rule)
        return [item.get(field_name, None) for item in export_table.get(source_key, [])]

    raise ValueError(f"Unsupported operation or invalid syntax for rule: {rule}")

# Example Usage
test_data = {
    "monthly_expenses": [
        {"month": "2024-07", "rent": 2000, "utilities": 350, "salaries": 5000, "marketing": 800},
        {"month": "2024-08", "rent": 2000, "utilities": 360, "salaries": 5200, "marketing": 850},
        {"month": "2024-09", "rent": 2100, "utilities": 370, "salaries": 5300, "marketing": 900}
    ],
    "customer_feedback": [
        {"date": "2024-08-01", "positive_feedback": 50, "negative_feedback": 5},
        {"date": "2024-08-02", "positive_feedback": 60, "negative_feedback": 7}
    ]
}

# Running rules
print(execute_rule(test_data, "sum(monthly_expenses.rent)"))                        # [6100]
print(execute_rule(test_data, "cumsum(monthly_expenses.salaries)"))                 # [5000, 10200, 15500]
print(execute_rule(test_data, "add_arrays(monthly_expenses.rent, monthly_expenses.utilities)"))  # [2350, 2360, 2470]
print(execute_rule(test_data, "softmax(customer_feedback.positive_feedback)"))     # Softmax result
print(execute_rule(test_data, "filter(monthly_expenses, 'salaries > 5100')"))      # Filters entries in monthly_expenses where salaries > 5100
print(execute_rule(test_data, "combine(customer_feedback.positive_feedback, monthly_expenses.marketing)")) # Combined result
print(execute_rule(test_data, "map(monthly_expenses.rent, x -> x * 1.1)"))          # Increase rent by 10%
print(execute_rule(test_data, "sort(monthly_expenses, 'salaries desc')"))           # Sort by salaries descending