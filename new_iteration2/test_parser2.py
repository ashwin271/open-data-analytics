import unittest

# Import the functions to be tested
from parser import (
    process_fn, fetch_data, calculate_percentages,
    parse_rule, fn_split, update_dict, add, flatten
)

class TestYourModule(unittest.TestCase):

    def test_process_fn(self):
        self.assertEqual(process_fn('sum', [[1, 2, 3]]), 6)
        self.assertEqual(process_fn('sum', [[-1, -2, -3]]), -6)
        self.assertEqual(process_fn('sum', [[0, 0, 0]]), 0)
        self.assertEqual(process_fn('sum', [[1]]), 1)
        self.assertEqual(process_fn('sum', [[]]), 0)
        self.assertEqual(process_fn('calculate_percentages', [[10], [20], [30]]), [16.666666666666664, 33.33333333333333, 50.0])
        self.assertEqual(process_fn('calculate_percentages', [[0], [0], [0]]), [0, 0, 0])
        self.assertEqual(process_fn('calculate_percentages', [[3]]), [100])
        self.assertEqual(process_fn('calculate_percentages', [[1, 2], [3, 4]]), [10.0, 20.0, 30.0, 40.0])
        with self.assertRaises(ValueError):
            process_fn('nonexistent_function', [[1, 2, 3]])

    def test_fetch_data(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        self.assertEqual(fetch_data('category1.field1', data), [10, 20])
        self.assertEqual(fetch_data('category2.field2', data), [30, 40])
        self.assertEqual(fetch_data('category1.field1', {}), [])
        self.assertEqual(fetch_data('category1.field1', {'category1': []}), [])
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field2': 10}]}), [])
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': '10'}, {'field1': '20'}]}), [10, 20])
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': 10}, {'field1': 20}, {'field1': 30}]}), [10, 20, 30])
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': 10}, {'field1': 20}, {'field2': 30}]}), [10, 20])
        self.assertEqual(fetch_data('category1.field1', {'category1': [{'field1': 10}, {'field1': 20}, {'field1': 30}, {'field1': 40}]}), [10, 20, 30, 40])
        with self.assertRaises(ValueError):
            fetch_data('invalid_query', data)

    def test_calculate_percentages(self):
        self.assertEqual(calculate_percentages([10], [20], [30]), [16.666666666666664, 33.33333333333333, 50.0])
        self.assertEqual(calculate_percentages([0], [0], [0]), [0, 0, 0])
        self.assertEqual(calculate_percentages([3]), [100])
        self.assertEqual(calculate_percentages([1, 2], [3, 4]), [10.0, 20.0, 30.0, 40.0])
        self.assertEqual(calculate_percentages([1, 1, 1]), [33.33333333333333, 33.33333333333333, 33.33333333333333])
        self.assertEqual(calculate_percentages([0]), [0])
        self.assertEqual(calculate_percentages([100, 200]), [33.33333333333333, 66.66666666666666])
        self.assertEqual(calculate_percentages([50, 50]), [50.0, 50.0])
        self.assertEqual(calculate_percentages([1, 99]), [1.0, 99.0])
        self.assertEqual(calculate_percentages([25, 75]), [25.0, 75.0])

    def test_fn_split(self):
        self.assertEqual(fn_split('sum(category1.field1)'), ('sum', 'category1.field1'))
        self.assertEqual(fn_split('category1.field1'), (None, None))
        self.assertEqual(fn_split('calculate_percentages(sum(category1.field1), sum(category2.field2))'), ('calculate_percentages', 'sum(category1.field1), sum(category2.field2)'))
        self.assertEqual(fn_split('field1'), (None, None))
        self.assertEqual(fn_split('sum(field1, field2)'), ('sum', 'field1, field2'))
        self.assertEqual(fn_split('calculate_percentages(field1, field2)'), ('calculate_percentages', 'field1, field2'))
        self.assertEqual(fn_split('field1.field2'), (None, None))
        self.assertEqual(fn_split('sum(field1.field2)'), ('sum', 'field1.field2'))
        self.assertEqual(fn_split('calculate_percentages(sum(field1.field2))'), ('calculate_percentages', 'sum(field1.field2)'))
        self.assertEqual(fn_split('field1.field2.field3'), (None, None))

    def test_parse_rule(self):
        data = {
            'category1': [{'field1': 10}, {'field1': 20}],
            'category2': [{'field2': 30}, {'field2': 40}]
        }
        self.assertEqual(parse_rule('sum(category1.field1)', data), 30)
        self.assertEqual(parse_rule('calculate_percentages(sum(category1.field1), sum(category2.field2))', data), [30.0, 70.0])
        self.assertEqual(parse_rule('category1.field1', data), [10, 20])
        self.assertEqual(parse_rule('calculate_percentages(sum(category1.field1), sum(category2.field2))', data), [30.0, 70.0])
        self.assertEqual(parse_rule('sum(category1.field1, category2.field2)', data), 100)
        self.assertEqual(parse_rule('calculate_percentages(category1.field1, category1.field1)', data), [16.666666666666664, 33.33333333333333, 16.666666666666664, 33.33333333333333])
        self.assertEqual(parse_rule('sum(category1.field1, category1.field1)', data), 60)
        self.assertEqual(parse_rule('calculate_percentages(category1.field1, category1.field1, category2.field2)', data), [7.6923076923076925, 15.384615384615385, 7.6923076923076925, 15.384615384615385, 23.076923076923077, 30.76923076923077])
        self.assertEqual(parse_rule('sum(category1.field1, category1.field1, category2.field2)', data), 130)
        with self.assertRaises(ValueError):
            parse_rule('invalid_function(category1.field1)', data)

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
        expected_dict = {
            'key1': 30,
            'key2': [[30, 70]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

        a_dict = {
            'key1': 'sum(category1.field1)',
            'key2': ['calculate_percentages(sum(category1.field1), sum(category2.field2))'],
            'key3': {
                'nested_key': 'category1.field1'
            }
        }
        expected_dict = {
            'key1': 30,
            'key2': [[30.0, 70.0]],
            'key3': {
                'nested_key': [10, 20]
            }
        }
        update_dict(a_dict, data)
        self.assertEqual(a_dict, expected_dict)

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
        self.assertEqual(add([1, 2, 3]), 6)
        self.assertEqual(add([[1, 2], [3, 4]]), 10)
        self.assertEqual(add([-1, -2, -3]), -6)
        self.assertEqual(add([]), 0)
        self.assertEqual(add([0, 0, 0]), 0)
        self.assertEqual(add([1]), 1)
        self.assertEqual(add([1, -1]), 0)
        self.assertEqual(add([1, 2, 3, 4, 5]), 15)
        self.assertEqual(add([10, 20, 30]), 60)
        self.assertEqual(add([100, 200, 300]), 600)

    def test_flatten(self):
        self.assertEqual(flatten([1, [2, [3, 4], 5], 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flatten(1), [1])
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[], []]), [])
        self.assertEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])
        self.assertEqual(flatten([1, [2, 3], 4]), [1, 2, 3, 4])
        self.assertEqual(flatten([1, [2, [3, [4, 5]]]]), [1, 2, 3, 4, 5])
        self.assertEqual(flatten([[[1, 2], 3], 4]), [1, 2, 3, 4])
        self.assertEqual(flatten([1, [2, [3, [4, [5]]]]]), [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()