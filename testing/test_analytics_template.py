test_analytics = {
    'database_1': [
        {
            'type': 'bar',
            'title': 'Sum of Field 1 vs Field 2',
            'data': {
                'x': 'table_1.field_1',
                'y': [
                    {'label': 'Field 2', 'expression': 'sum(table_1.field_2)'},
                    # Add more y-expressions
                ]
            },
            'axes': {'x_label': 'Field 1', 'y_label': 'Sum of Field 2'}
        },
        # Add more analytics templates for database_1
    ],
    'database_2': [
        {
            'type': 'line',
            'title': 'Sum of Field 4 vs Field 5',
            'data': {
                'x': 'table_3.field_4',
                'y': [
                    {'label': 'Field 5', 'expression': 'sum(table_3.field_5)'},
                    # Add more y-expressions
                ]
            },
            'axes': {'x_label': 'Field 4', 'y_label': 'Sum of Field 5'}
        },
        # Add more analytics templates for database_2
    ],
    # Add more databases and their corresponding templates as needed
}
