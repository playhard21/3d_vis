import json


# Function to transform a single JSON data entry
def transform_json_data(data):
    # Initialize lists to hold the values for Dry_Fractures and Yielding_Fractures
    dry_fractures = []
    yielding_fractures = []

    # Collect the value of "Dry_Fractures" first if it exists and is not None
    if data.get("Dry_Fractures") is not None:
        dry_fractures.append(data.get("Dry_Fractures"))

    # Collect the value of "Yielding_Fractures" first if it exists and is not None
    if data.get("Yielding_Fractures") is not None:
        yielding_fractures.append(data.get("Yielding_Fractures"))

    # Iterate through the data dictionary
    for key, value in data.items():
        # Check if the key is one of the 'Unnamed' fields and its value is not None
        if "Unnamed" in key and value is not None:
            # Determine if the key belongs to Dry_Fractures or Yielding_Fractures
            unnamed_number = int(key.split(":")[1])
            if 9 <= unnamed_number <= 13:
                dry_fractures.append(value)  # Append the value to Dry_Fractures
            elif 15 <= unnamed_number <= 22:
                yielding_fractures.append(value)  # Append the value to Yielding_Fractures

    # Create a new dictionary with the transformed structure
    transformed_data = {
        "BW_ID": data.get("BW_ID"),
        "LAT": data.get("LAT"),
        "LONG": data.get("LONG"),
        "Elevation_masl": data.get("Elevation_masl"),
        "Well_depth_m_bgl": data.get("Well_depth_m_bgl"),
        "SWL_2016_mbgl": data.get("SWL_2016_mbgl"),
        "SWL_2017_m_bgl": data.get("SWL_2017_m_bgl"),
        "Casing_end_m_bgl": data.get("Casing_end_m_bgl"),
        "Dry_Fractures": dry_fractures,
        "Yielding_Fractures": yielding_fractures
    }

    return transformed_data



# Read the JSON data from a file
with open('data/data.json', 'r') as f:
    json_data = json.load(f)

# Check if json_data is a list
if isinstance(json_data, list):
    # Transform each item in the list
    transformed_data_list = [transform_json_data(item) for item in json_data]
else:
    # Transform the single JSON object
    transformed_data_list = [transform_json_data(json_data)]

# Write the transformed data back to a JSON file
with open('matplot/transformed_data.json', 'w') as f:
    json.dump(transformed_data_list, f, indent=2)

print("JSON data has been transformed and saved to 'transformed_data.json'.")