# Notebook: Data Visualization with Parsing Syntax

# Cell 1: Import Necessary Libraries
import matplotlib.pyplot as plt
import numpy as np

# Cell 2: Define the data_visualizer Function
def data_visualizer(data):
    graph_type = data.get("type", "").lower()
    title = data.get("title", "Chart")
    
    if graph_type == "bar":
        x_axis = data["x_values"]["values"]
        y_axis_label = data["axes"]["y"]["label"]
        series = data["data"]
        
        bar_width = 0.35
        indices = np.arange(len(x_axis))
        
        fig, ax = plt.subplots()
        
        for idx, serie in enumerate(series):
            ax.bar(indices + idx * bar_width, serie["y_values"]["values"], bar_width, label=serie["label"])

        ax.set_xlabel(data["axes"]["x"]["label"])
        ax.set_ylabel(y_axis_label)
        ax.set_title(title)
        ax.set_xticks(indices + bar_width / 2)
        ax.set_xticklabels(x_axis)
        ax.legend()
        plt.show()

    elif graph_type == "scatter":
        fig, ax = plt.subplots()
        
        for serie in data["data"]:
            ax.scatter(serie["x_points"]["values"], serie["y_points"]["values"], label=serie["label"])

        ax.set_xlabel(data["axes"]["x"]["label"])
        ax.set_ylabel(data["axes"]["y"]["label"])
        ax.set_title(title)
        ax.legend()
        plt.show()

    elif graph_type == "line":
        x_axis = data["x_values"]["values"]
        
        fig, ax = plt.subplots()
        
        for serie in data["data"]:
            ax.plot(x_axis, serie["y_values"]["values"], label=serie["label"])
            
        ax.set_xlabel(data["axes"]["x"]["label"])
        ax.set_ylabel(data["axes"]["y"]["label"])
        ax.set_title(title)
        ax.legend()
        plt.show()

    elif graph_type == "pie":
        labels = data["data"]["labels"]["values"]
        sizes = data["data"]["percentages"]["values"]
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title(title)
        plt.axis('equal')
        plt.show()

    elif graph_type == "histogram":
        values = data["data"]["values"]
        
        fig, ax = plt.subplots()
        ax.hist(values, bins=10, edgecolor='black')
        ax.set_xlabel(data["axes"]["x"]["label"])
        ax.set_ylabel(data["axes"]["y"]["label"])
        ax.set_title(title)
        plt.show()

    elif graph_type == "boxplot":
        categories = data["axes"]["x"]["values"]
        data_series = [data["data"][category]["values"] for category in categories]
        
        fig, ax = plt.subplots()
        ax.boxplot(data_series, labels=categories)
        ax.set_xlabel(data["axes"]["x"]["label"])
        ax.set_ylabel(data["axes"]["y"]["label"])
        ax.set_title(title)
        plt.show()
    else:
        raise ValueError(f"Unsupported graph type: {graph_type}")

# Cell 3: Visualize Bar Graph Data
pre_parsed_data_bar = {
    "type": "bar",
    "title": "Monthly Salary Expenses",
    "axes": {
        "x": {
            "label": "Month"
        },
        "y": {
            "label": "Salaries"
        }
    },
    "x_values": {
        "values": ["July", "August", "September"]
    },
    "data": [
        {
            "label": "Monthly Salaries",
            "y_values": {
                "values": "monthly_expenses.salaries"
            }
        }
    ]
}

# Assume parser operation here
parsed_output_data_bar = {
    "type": "bar",
    "title": "Monthly Salary Expenses",
    "axes": {
        "x": {
            "label": "Month"
        },
        "y": {
            "label": "Salaries ($)"
        }
    },
    "x_values": {
        "values": ["July", "August", "September"]
    },
    "data": [
        {
            "label": "Monthly Salaries",
            "y_values": {
                "values": [5000, 5200, 5300]
            }
        }
    ]
}

data_visualizer(parsed_output_data_bar)

# Cell 4: Visualize Pie Chart Data
pre_parsed_data_pie = {
    "type": "pie",
    "title": "Feedback Distribution",
    "data": {
        "labels": {
            "values": "customer_feedback.date"
        },
        "percentages": {
            "values": "map(customer_feedback.positive_feedback, feedback -> feedback * 1.0)"
        }
    }
}

# Assume parser operation here
parsed_output_data_pie = {
    "type": "pie",
    "title": "Feedback Distribution",
    "data": {
        "labels": {
            "values": ["2024-08-01", "2024-08-02", "2024-08-03", "2024-08-04", "2024-08-05"]
        },
        "percentages": {
            "values": [50, 60, 70, 55, 65]
        }
    }
}

data_visualizer(parsed_output_data_pie)

# Cell 5: Visualize Line Graph Data
pre_parsed_data_line = {
    "type": "line",
    "title": "Daily Food Sales Trends",
    "axes": {
        "x": {
            "label": "Date"
        },
        "y": {
            "label": "Food Sales"
        }
    },
    "x_values": {
        "values": "daily_operations.date"
    },
    "data": [
        {
            "label": "Food Sales Over Time",
            "y_values": {
                "values": "daily_operations.food_sales"
            }
        }
    ]
}

# Assume parser operation here
parsed_output_data_line = {
    "type": "line",
    "title": "Daily Food Sales Trends",
    "axes": {
        "x": {
            "label": "Date"
        },
        "y": {
            "label": "Food Sales ($)"
        }
    },
    "x_values": {
        "values": ["2024-08-01", "2024-08-02", "2024-08-03", "2024-08-04", "2024-08-05"]
    },
    "data": [
        {
            "label": "Food Sales Over Time",
            "y_values": {
                "values": [1500, 1600, 1700, 1400, 1550]
            }
        }
    ]
}

data_visualizer(parsed_output_data_line)

# Cell 6: Visualize Scatter Plot Data
pre_parsed_data_scatter = {
    "type": "scatter",
    "title": "Beverage vs Dessert Sales",
    "axes": {
        "x": {
            "label": "Beverage Sales"
        },
        "y": {
            "label": "Dessert Sales"
        }
    },
    "data": [
        {
            "label": "Sales Correlation",
            "x_points": {
                "values": "daily_operations.beverage_sales"
            },
            "y_points": {
                "values": "daily_operations.dessert_sales"
            }
        }
    ]
}

# Assume parser operation here
parsed_output_data_scatter = {
    "type": "scatter",
    "title": "Beverage vs Dessert Sales",
    "axes": {
        "x": {
            "label": "Beverage Sales ($)"
        },
        "y": {
            "label": "Dessert Sales ($)"
        }
    },
    "data": [
        {
            "label": "Sales Correlation",
            "x_points": {
                "values": [600, 700, 750, 650, 620]
            },
            "y_points": {
                "values": [400, 420, 430, 415, 405]
            }
        }
    ]
}

data_visualizer(parsed_output_data_scatter)

# Cell 7: Visualize Histogram Data
pre_parsed_data_histogram = {
    "type": "histogram",
    "title": "Distribution of Ingredient Costs",
    "axes": {
        "x": {
            "label": "Cost"
        },
        "y": {
            "label": "Frequency"
        }
    },
    "data": {
        "values": "inventory_management.ingredients_cost"
    }
}

# Assume parser operation here
parsed_output_data_histogram = {
    "type": "histogram",
    "title": "Distribution of Ingredient Costs",
    "axes": {
        "x": {
            "label": "Cost ($)"
        },
        "y": {
            "label": "Frequency"
        }
    },
    "data": {
        "values": [750, 780, 790, 760, 770]
    }
}

data_visualizer(parsed_output_data_histogram)

# Cell 8: Visualize Box Plot Data
pre_parsed_data_boxplot = {
    "type": "boxplot",
    "title": "Monthly Expenses Distribution",
    "axes": {
        "x": {
            "label": "Expense Category",
            "values": ["Rent", "Utilities", "Salaries", "Marketing"]
        },
        "y": {
            "label": "Cost"
        }
    },
    "data": {
        "rent": {
            "values": "monthly_expenses.rent"
        },
        "utilities": {
            "values": "monthly_expenses.utilities"
        },
        "salaries": {
            "values": "monthly_expenses.salaries"
        },
        "marketing": {
            "values": "monthly_expenses.marketing"
        }
    }
}

# Assume parser operation here
parsed_output_data_boxplot = {
    "type": "boxplot",
    "title": "Monthly Expenses Distribution",
    "axes": {
        "x": {
            "label": "Expense Category",
            "values": ["Rent", "Utilities", "Salaries", "Marketing"]
        },
        "y": {
            "label": "Cost ($)"
        }
    },
    "data": {
        "rent": {
            "values": [2000, 2000, 2100]
        },
        "utilities": {
            "values": [350, 360, 370]
        },
        "salaries": {
            "values": [5000, 5200, 5300]
        },
        "marketing": {
            "values": [800, 850, 900]
        }
    }
}

data_visualizer(parsed_output_data_boxplot)
