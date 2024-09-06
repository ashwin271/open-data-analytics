import unittest

# Import the functions to be tested
from parser import (
    process_fn, fetch_data, calculate_percentages,
    parse_rule, fn_split, update_dict, add, flatten
)

class TestYourModule(unittest.TestCase):

    def test_process_fn(self):
        # Test sum function with positive numbers
        self.assertEqual(process_fn('sum', [[1, 2, 3]]), 6)
        # Test sum function with negative numbers
        self.assertEqual(process_fn('sum', [[-1, -2, -3]]), -6)
        # Test sum function with zeros
        self.assertEqual(process_fn('sum', [[0, 0, 0]]), 0)
        # Test sum function with a single element
        self.assertEqual(process_fn('sum', [[1]]), 1)
        # Test sum function with an empty list
        self.assertEqual(process_fn('sum', [[]]), 0)
        
        # Test calculate_percentages function with different values
        self.assertEqual(process_fn('calculate_percentages', [[10], [20], [30]]), [16.666666666666664, 33.33333333333333, 50.0])
        # Test calculate_percentages function with zeros
        self.assertEqual(process_fn('calculate_percentages', [[0], [0], [0]]), [0, 0, 0])
        # Test calculate_percentages function with a single value
        self.assertEqual(process_fn('calculate_percentages', [[3]]), [100])
        # Test calculate_percentages function with multiple lists
        self.assertEqual(process_fn('calculate_percentages', [[1, 2], [3, 4]]), [10.0, 20.0, 30.0, 40.0])
        
        # Test nonexistent function
        with self.assertRaises(ValueError):
            process_fn('nonexistent_function', [[1, 2, 3]])

    def test_fetch_data(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        
        # Test valid query for category1.field1
        self.assertEqual(fetch_data('category1.field1', data), [10, 20])
        # Test valid query for category2.field2
        self.assertEqual(fetch_data('category2.field2', data), [30, 40])
        
        # Test query with empty data
        self.assertEqual(fetch_data('category1.field1', {}), [])
        # Test query with empty category
        self.assertEqual(fetch_data('category1.field1', {'category1': []}), [])
        
        # Test query with missing fields
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field2': 10}]}), [])
        
        # Test query with string values
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': '10'}, {'field1': '20'}]}), [10, 20])
        
        # Test query with mixed fields
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': 10}, {'field1': 20}, {'field2': 30}]}), [10, 20])
        
        # Test invalid query
        with self.assertRaises(ValueError):
            fetch_data('invalid_query', data)

    def test_calculate_percentages(self):
        # Test calculate_percentages with different values
        self.assertEqual(calculate_percentages([10], [20], [30]), [16.666666666666664, 33.33333333333333, 50.0])
        # Test calculate_percentages with zeros
        self.assertEqual(calculate_percentages([0], [0], [0]), [0, 0, 0])
        # Test calculate_percentages with a single value
        self.assertEqual(calculate_percentages([3]), [100])
        # Test calculate_percentages with multiple lists
        self.assertEqual(calculate_percentages([1, 2], [3, 4]), [10.0, 20.0, 30.0, 40.0])
        # Test calculate_percentages with repeated values
        self.assertEqual(calculate_percentages([1, 1, 1]), [33.33333333333333, 33.33333333333333, 33.33333333333333])
        # Test calculate_percentages with a single zero
        self.assertEqual(calculate_percentages([0]), [0])
        # Test calculate_percentages with two values
        self.assertEqual(calculate_percentages([100, 200]), [33.33333333333333, 66.66666666666666])
        # Test calculate_percentages with equal values
        self.assertEqual(calculate_percentages([50, 50]), [50.0, 50.0])
        # Test calculate_percentages with highly skewed values
        self.assertEqual(calculate_percentages([1, 99]), [1.0, 99.0])
        # Test calculate_percentages with a 25-75 split
        self.assertEqual(calculate_percentages([25, 75]), [25.0, 75.0])

    def test_fn_split(self):
        # Test function and field extraction for sum
        self.assertEqual(fn_split('sum(category1.field1)'), ('sum', 'category1.field1'))
        # Test function and field extraction for a simple field
        self.assertEqual(fn_split('category1.field1'), (None, None))
        # Test function and field extraction for nested functions
        self.assertEqual(fn_split('calculate_percentages(sum(category1.field1), sum(category2.field2))'), ('calculate_percentages', 'sum(category1.field1), sum(category2.field2)'))
        # Test function and field extraction for a simple field
        self.assertEqual(fn_split('field1'), (None, None))
        # Test function and field extraction for sum with multiple fields
        self.assertEqual(fn_split('sum(field1, field2)'), ('sum', 'field1, field2'))
        # Test function and field extraction for calculate_percentages with multiple fields
        self.assertEqual(fn_split('calculate_percentages(field1, field2)'), ('calculate_percentages', 'field1, field2'))
        # Test function and field extraction for nested fields
        self.assertEqual(fn_split('field1.field2'), (None, None))
        # Test function and field extraction for sum with nested fields
        self.assertEqual(fn_split('sum(field1.field2)'), ('sum', 'field1.field2'))
        # Test function and field extraction for calculate_percentages with nested sum
        self.assertEqual(fn_split('calculate_percentages(sum(field1.field2))'), ('calculate_percentages', 'sum(field1.field2)'))
        # Test function and field extraction for deeply nested fields
        self.assertEqual(fn_split('field1.field2.field3'), (None, None))

    def test_parse_rule(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        
        # Test parsing and evaluating sum rule
        self.assertEqual(parse_rule('sum(category1.field1)', data), 30)
        # Test parsing and evaluating calculate_percentages rule with sums
        self.assertEqual(parse_rule('calculate_percentages(sum(category1.field1), sum(category2.field2))', data), [30.0, 70.0])
        # Test parsing and evaluating simple field rule
        self.assertEqual(parse_rule('category1.field1', data), [10, 20])
        # Test parsing and evaluating sum rule with multiple fields
        self.assertEqual(parse_rule('sum(category1.field1, category2.field2)', data), 100)
        # Test parsing and evaluating calculate_percentages rule with repeated fields
        self.assertEqual(parse_rule('calculate_percentages(category1.field1, category1.field1)', data), [16.666666666666664, 33.33333333333333, 16.666666666666664, 33.33333333333333])
        # Test parsing and evaluating sum rule with repeated fields
        self.assertEqual(parse_rule('sum(category1.field1, category1.field1)', data), 60)
        # Test parsing and evaluating calculate_percentages rule with multiple fields
        self.assertEqual(parse_rule('calculate_percentages(category1.field1, category1.field1, category2.field2)', data), [7.6923076923076925, 15.384615384615385, 7.6923076923076925, 15.384615384615385, 23.076923076923077, 30.76923076923077])
        # Test parsing and evaluating sum rule with multiple repeated fields
        self.assertEqual(parse_rule('sum(category1.field1, category1.field1, category2.field2)', data), 130)
        
        # Test invalid function
        with self.assertRaises(ValueError):
            parse_rule('invalid_function(category1.field1)', data)

    def test_update_dict(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        
        # Test updating dictionary with calculated sum and percentages
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(sum(category1.field1), sum(category2.field2))'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[30, 70]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for a single field
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1)'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[33.33333333333333, 66.66666666666666]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for a field and its sum
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1, sum(category1.field1))'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[16.666666666666664, 33.33333333333333, 50.0]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for multiple fields and sums
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1, sum(category1.field1), sum(category2.field2))'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[7.6923076923076925, 15.384615384615385, 23.076923076923077, 53.84615384615385]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for repeated fields
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1, category1.field1)'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[16.666666666666664, 33.33333333333333, 16.666666666666664, 33.33333333333333]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for multiple repeated fields
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1, category1.field1, category1.field1, category2.field2)'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[6.25, 12.5, 6.25, 12.5, 6.25, 12.5, 18.75, 25.0]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        # Test updating dictionary with calculated percentages for multiple repeated fields and sums
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(category1.field1, category1.field1, category1.field1, category1.field1, category2.field2)'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[5.263157894736842, 10.526315789473683, 5.263157894736842, 10.526315789473683, 5.263157894736842, 10.526315789473683, 5.263157894736842, 10.526315789473683, 15.789473684210526, 21.052631578947366]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

    def test_add(self):
        # Test adding a list of positive numbers
        self.assertEqual(add([1, 2, 3]), 6)
        # Test adding nested lists of positive numbers
        self.assertEqual(add([[1, 2], [3, 4]]), 10)
        # Test adding a list of negative numbers
        self.assertEqual(add([-1, -2, -3]), -6)
        # Test adding an empty list
        self.assertEqual(add([]), 0)
        # Test adding a list of zeros
        self.assertEqual(add([0, 0, 0]), 0)
        # Test adding a single element list
        self.assertEqual(add([1]), 1)
        # Test adding a list with positive and negative numbers
        self.assertEqual(add([1, -1]), 0)
        # Test adding a longer list of positive numbers
        self.assertEqual(add([1, 2, 3, 4, 5]), 15)
        # Test adding a list of larger positive numbers
        self.assertEqual(add([10, 20, 30]), 60)
        # Test adding a list of even larger positive numbers
        self.assertEqual(add([100, 200, 300]), 600)

    def test_flatten(self):
        # Test flattening a nested list
        self.assertEqual(flatten([1, [2, [3, 4], 5], 6]), [1, 2, 3, 4, 5, 6])
        # Test flattening a flat list
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])
        # Test flattening a single element
        self.assertEqual(flatten(1), [1])
        # Test flattening an empty list
        self.assertEqual(flatten([]), [])
        # Test flattening a list of empty lists
        self.assertEqual(flatten([[], []]), [])
        # Test flattening a list of lists
        self.assertEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])
        # Test flattening a list with nested lists
        self.assertEqual(flatten([1, [2, 3], 4]), [1, 2, 3, 4])
        # Test flattening a deeply nested list
        self.assertEqual(flatten([1, [2, [3, [4, 5]]]]), [1, 2, 3, 4, 5])
        # Test flattening a list with nested lists and elements
        self.assertEqual(flatten([[[1, 2], 3], 4]), [1, 2, 3, 4])
        # Test flattening a list with multiple levels of nesting
        self.assertEqual(flatten([1, [2, [3, [4, [5]]]]]), [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()