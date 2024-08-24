# How to Use the Workflow Visualization Script

This document provides a guide to setting up and using the Python script for fetching and visualizing workflow templates from a remote server.

## Prerequisites

Before running the script, make sure you have the following:

- **Python**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Required Python Packages**: Install the required packages using pip. This could include `requests` and any additional packages for your `visualizer` module if needed.

```bash
pip install requests
# Add any other necessary packages for the visualizer
```

## Script Setup

1. **Clone the Repository**: Clone or download the repository containing the script to your local machine.

2. **File Structure**: Ensure that `visualizer.py` is in the same directory as the script or is accessible via the `PYTHONPATH`. The `visualizer` module is assumed to contain the function `create_plot` for generating plot images from analytics data.

3. **Set Base URL**: Edit the `BASE_URL` variable in the script to point to the correct API endpoint (replace `https://example.com/api` with your actual base URL).

## Running the Script

You can run the script with either default or custom parameters.

### Running with Default Parameters

Simply execute the script from your terminal. This will use the default `job_id` and `uid` set in the script:

```bash
python script_name.py
```

### Running with Custom Parameters

To supply custom `job_id` and `uid`, use the following command syntax:

```bash
python script_name.py --job_id <your_job_id> --uid <your_user_id>
```

### Example Run

```bash
python script_name.py --job_id 67890 --uid user456
```

## Output

- **Workflow Details**: The script will print the workflow template name and report fetched from the API.
- **Visualizations**: Any visualizations generated from the analytics object will be saved to the `visualizations` directory with filenames such as `plot_0.png`, `plot_1.png`, etc.

## Error Handling

- **Invalid Data**: If the workflow template name or report is missing, a `ValueError` will be raised with a descriptive message.
- **Request Failures**: Any network or server-related failures during the API requests will raise a `requests.exceptions.RequestException`.

## Troubleshooting

- If you encounter issues with the API requests, ensure that the base URL and parameters are correctly set.
- Verify that all required packages are installed and up-to-date.
- Ensure that the `visualizer.py` module is correctly implemented and accessible.
