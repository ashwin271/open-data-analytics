analytics = [
    {
        "title": "Total Inventory Comparison",
        "type": "bar",
        "axes": {
            "x_label": "Stage",
            "y_label": "Total Inventory"
        },
        "data": {
            "x": "warehouse_to_shop.item_id",
            "y": [
                {
                    "label": "Warehouse",
                    "values": "warehouse_to_shop.warehouse_total_inventory"
                },
                {
                    "label": "Shop",
                    "values": "warehouse_to_shop.shop_total_inventory"
                },
                {
                    "label": "Sales",
                    "values": "shop_to_sales.sales_total_inventory"
                }
            ]
        }
    },
    # {
    #   "name": "inventory_trend_line",
    #   "type": "line",
    #   "title": "Inventory Reconciliation Trend",
    #   "axes": {
    #     "x": {
    #       "label": "Date",
    #       "values": "shop_to_sales.date"
    #     },
    #     "y": {
    #       "label": "Inventory"
    #     }
    #   },
    #   "data": [
    #     {
    #       "label": "Inventory",
    #       "y_values": "list(shop_to_sales.inventory_difference)"
    #     }
    #   ]
    # },
    # {
    #   "name": "product_distribution_pie",
    #   "type": "pie",
    #   "title": "Product Distribution",
    #   "data": [
    #     {
    #       "label": "Distribution",
    #       "values": [
    #         {
    #           "name": "Product A",
    #           "value": "sum(filter(shop_to_sales.sales_total_inventory, product='A'))"
    #         },
    #         {
    #           "name": "Product B",
    #           "value": "sum(filter(shop_to_sales.sales_total_inventory, product='B'))"
    #         },
    #         {
    #           "name": "Product C",
    #           "value": "sum(filter(shop_to_sales.sales_total_inventory, product='C'))"
    #         }
    #       ]
    #     }
    #   ]
    # }
]
