from src.api_client import view_template
from parser import update_dict
from typing import Dict, Any, List

def analyse_reconciliation(
    export_table: Dict[str, Any],
    data: Dict[str, Any]
) -> Dict[str, Any]:
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

    def process_workflow_analytics(workflow_template: Dict[str, Any], dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processes the analytics templates in the workflow."""
        processed_analytics_results = []

        # Check if the analytics object exists in the workflow template
        if 'analytics' in workflow_template:
            # Process each analytics template with the provided dataset
            for analytics_template in workflow_template['analytics']:
                update_dict(analytics_template, dataset)
                processed_analytics_results.append(analytics_template)
        
        return processed_analytics_results

    # Fetch the workflow template based on provided data
    workflow_template = get_workflow_template(data)

    # Process the analytics in the workflow template
    processed_analytics = process_workflow_analytics(workflow_template, export_table)

    # Return the processed analytics results
    return {
        "workflow_template_name": data["workflow_template_name"],
        "processed_analytics": processed_analytics
    }
