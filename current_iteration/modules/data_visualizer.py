import matplotlib.pyplot as plt
import numpy as np

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
