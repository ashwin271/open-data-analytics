from parser import update_dict
from analytics_template import analytics
from dataset import data
from pprint import pprint

def main():
    # Update the analytics templates with the actual data
    for template in analytics:
        update_dict(template, data)
    
    # Print or process the updated analytics templates
    for template in analytics:
        pprint(template)

if __name__ == "__main__":
    main()
