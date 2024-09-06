import unittest

# Import the functions to be tested
from parser import (
    process_fn, fetch_data, calculate_percentages,
    parse_rule, fn_split, update_dict, add, flatten
)

class TestYourModule(unittest.TestCase):

    def test_process_fn(self):
        self.assertEqual(process_fn('sum', [[1, 2, 3]]), 6)
        with self.assertRaises(ValueError):
            process_fn('nonexistent_function', [[1, 2, 3]])

    def test_fetch_data(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        self.assertEqual(fetch_data('category1.field1', data), [10, 20])
        self.assertEqual(fetch_data('category2.field2', data), [30, 40])
        with self.assertRaises(ValueError):
            fetch_data('invalid_query', data)

    def test_calculate_percentages(self):
        self.assertEqual(calculate_percentages([10], [20], [30]), [16.666666666666664, 33.33333333333333, 50.0])
        self.assertEqual(calculate_percentages([0], [0], [0]), [0, 0, 0])
        self.assertEqual(calculate_percentages([3]), [100])

    def test_fn_split(self):
        self.assertEqual(fn_split('sum(category1.field1)'), ('sum', 'category1.field1'))
        self.assertEqual(fn_split('category1.field1'), (None, None))

    def test_parse_rule(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        self.assertEqual(parse_rule('sum(category1.field1)', data), 30)
        self.assertEqual(parse_rule('calculate_percentages(sum(category1.field1), sum(category2.field2))', data), [30, 70])

    def test_update_dict(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(sum(category1.field1), sum(category2.field2))'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        # Expected result after processing the dictionary
        expected_dict = {
            'key1': 30,
            'key2': [[30, 70]],
            'key3': {
                'nested_key': [10, 20]
            }
        }

        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

    # Additional tests for add and flatten functions
    def test_add(self):
        self.assertEqual(add([1, 2, 3]), 6)
        self.assertEqual(add([[1, 2], [3, 4]]), 10)

    def test_flatten(self):
        self.assertEqual(flatten([1, [2, [3, 4], 5], 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flatten(1), [1])

if __name__ == '__main__':
    unittest.main()