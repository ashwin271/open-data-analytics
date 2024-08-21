from typing import Callable, List, Dict, Any, Tuple, Union
import numpy as np

# Define types
OperationFunction = Callable[[List[float]], float]
TransformationFunction = Callable[[List[float]], List[float]]

# Registries for operations
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
    "log": transform_log,
    "cumsum": transform_cumsum,
    "add_arrays": elementwise_add,
})

def parse_field_identifier(identifier: str) -> Tuple[str, str]:
    try:
        collection_name, field_name = identifier.split('.', 1)
        return collection_name.strip(), field_name.strip()
    except ValueError:
        raise ValueError(f"Invalid field identifier: {identifier}")

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
    if '(' in rule:
        func_name, args_string = rule.split("(", 1)
        args_string = args_string.rstrip(")")
        return func_name.strip(), split_arguments(args_string)
    else:
        return rule.strip(), []

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

# Utility to safely evaluate map expressions
def safe_eval(expr, value):
    if value is None:
        raise ValueError("Value for mapping is None")
    expression = expr.replace("x", str(value))
    return eval(expression, {"__builtins__": None}, {})

# Rule Execution
def execute_rule(working_data: Dict[str, List[Dict[str, Any]]], rule: str) -> List[Any]:
    func_name, args = parse_rule(rule)

    if func_name in aggregation_functions:
        source_key, field_name = parse_field_identifier(args[0])
        field_values = [item.get(field_name, 0) for item in working_data.get(source_key, [])]
        return [aggregation_functions[func_name](field_values)]

    elif func_name in transformation_functions:
        if func_name == 'add_arrays':
            array1_values = execute_rule(working_data, args[0])
            array2_values = execute_rule(working_data, args[1])
            return transformation_functions[func_name](array1_values, array2_values)
        else:
            values = execute_rule(working_data, args[0])
            return transformation_functions[func_name](values)

    elif func_name == 'filter':
        source_key, condition = args
        collection = working_data.get(source_key, [])
        return filter_data(collection, condition)

    elif func_name == 'combine':
        combined_result = []
        for arg in args:
            combined_result.extend(execute_rule(working_data, arg))
        return combined_result

    elif func_name == 'map':
        collection_identifier, map_expr = args
        source_key, field_name = parse_field_identifier(collection_identifier)
        collection = [item.get(field_name, 0) for item in working_data.get(source_key, [])]
        
        # Extract the mapping expression
        map_expr = map_expr.split("->")[1].strip()
        return [safe_eval(map_expr, x) for x in collection]

    elif func_name == 'sort':
        # Expected format `sort(source_key, 'field_name desc')`
        source_key, sort_rule = args
        collection = working_data.get(source_key, [])
        field, order = sort_rule.split()
        reverse = order.lower() == 'desc'
        return sorted(collection, key=lambda x: x[field], reverse=reverse)

    elif '.' in rule:
        source_key, field_name = parse_field_identifier(rule)
        collection = working_data.get(source_key, [])
        if collection is None:
            raise ValueError(f"No data found for source key '{source_key}'.")
        return [item.get(field_name, None) for item in collection]

    raise ValueError(f"Unsupported operation or invalid syntax for rule: {rule}")