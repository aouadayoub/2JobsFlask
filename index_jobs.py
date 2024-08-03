import json

def index_job_data(json_path):
    """
    Reads job data from a JSON file and adds unique IDs.
    Saves the indexed data to a new JSON file.

    Args:
        json_path (str): Path to the input JSON file.
    """
    with open(json_path, 'r') as f:
        job_data = json.load(f)

    # Generate unique IDs
    for i, job in enumerate(job_data):
        job['id'] = i + 1  # Simple sequential ID (adjust as needed)

    # Save indexed data to a new JSON file
    with open("indexed_job_data.json", 'w') as f:
        json.dump(job_data, f, indent=4)

# Example usage
json_path = "job_data.json"  # Replace with your actual file path
index_job_data(json_path)

print(f"Indexed job data saved to indexed_job_data.json")