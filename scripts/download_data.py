import requests
import os

# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

def download_traffic_collision_data(output_csv_path="data/traffic_collisions_data.csv"):
    """
    Downloads Toronto Traffic Collision data from the Open Data Portal
    and saves it as a CSV file locally.

    Args:
        output_csv_path (str): File path where CSV will be saved.
    """
    # Base URL for Toronto CKAN API
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

    # API endpoint to get package (dataset) metadata
    url = base_url + "/api/3/action/package_show"
    params = { "id": "police-annual-statistical-report-traffic-collisions" }

    # Fetch the dataset package metadata
    response = requests.get(url, params=params)
    response.raise_for_status()
    package = response.json()

    # Look for the datastore-active resources
    for idx, resource in enumerate(package["result"]["resources"]):

        if resource["datastore_active"]:
            # Get all records as CSV
            csv_url = base_url + "/datastore/dump/" + resource["id"]
            resource_dump_data = requests.get(csv_url).text

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

            # Save the CSV content
            with open(output_csv_path, "w", encoding="utf-8") as f:
                f.write(resource_dump_data)

            print(f"✅ Traffic collision data downloaded and saved to: {output_csv_path}")
            return  # We found and saved the first active resource — stop here.

    print("❌ No datastore-active resources found for this dataset.")

if __name__ == "__main__":
    download_traffic_collision_data()
