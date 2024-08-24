import os
import requests
from typing import Dict, Any
from viz import create_plot  # Ensure viz.py is in the same directory or in PYTHONPATH
import argparse

BASE_URL = "https://example.com/api"  # Replace with the actual base URL

def view_reconciliation_job(job_id: str, uid: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/reconciliations/{job_id}"
    params = {"uid": uid}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def view_template(workflow_template_name: str, uid: str, scope: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/workflow_templates/{workflow_template_name}"
    params = {"uid": uid, "scope": scope}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_workflow_template(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fetches the workflow template."""
    try:
        return view_template(
            data["workflow_template_name"], data["uid"], "private"
        )["data"]
    except Exception:
        try:
            return view_template(
                data["workflow_template_name"], data["uid"], "public"
            )["data"]
        except Exception:
            raise ValueError(
                f"Workflow {data['workflow_template_name']} not found in any scope"
            )

def get_analytics_object_from_template(workflow_template: Dict[str, Any]) -> Any:
    """Extracts the analytics object from the workflow template data."""
    analytics_object = workflow_template.get("analytics")
    
    if analytics_object is None:
        raise ValueError("Analytics object not found in the workflow template data.")
    
    return analytics_object

def get_workflow_template_and_report(job_id: str, uid: str) -> Dict[str, Any]:
    # Fetch the reconciliation job data
    job_data = view_reconciliation_job(job_id, uid)
    
    # Extract the 'workflow_template_name' and 'report' from the job data
    workflow_template_name = job_data.get("workflow_template_name")
    report = job_data.get("report")
    
    if workflow_template_name is None or report is None:
        raise ValueError("Workflow template name or report not found in the reconciliation job data.")
    
    # Get the workflow template data
    workflow_template_data = get_workflow_template({
        "workflow_template_name": workflow_template_name, 
        "uid": uid
    })
    
    # Get the analytics object from the workflow template data
    analytics_object = get_analytics_object_from_template(workflow_template_data)
    
    return {
        "workflow_template_name": workflow_template_name,
        "report": report,
        "analytics": analytics_object
    }

def visualize_analytics(analytics):
    visualization_folder = "visualizations"
    os.makedirs(visualization_folder, exist_ok=True)
    
    for index, plot_data in enumerate(analytics):
        save_path = os.path.join(visualization_folder, f"plot_{index}.png")
        create_plot(plot_data, save_path)
        print(f"Saved: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and visualize workflow template")
    parser.add_argument("--job_id", default="12345", help="Job ID to process (default: 12345)")
    parser.add_argument("--uid", default="user123", help="User ID (default: user123)")

    args = parser.parse_args()
    job_id = args.job_id
    uid = args.uid
    
    try:
        result = get_workflow_template_and_report(job_id, uid)
        print("Workflow Template Name:", result["workflow_template_name"])
        print("Report:", result["report"])
        
        # Visualize the analytics data
        visualize_analytics(result["analytics"])
        
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print("Failed to fetch data:", e)
