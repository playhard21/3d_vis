import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# Function to load the transformed JSON data
def load_transformed_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Load the transformed data
data_list = load_transformed_json('transformed_data.json')

# Extract and prepare data for plotting
lats = np.array([data['LAT'] for data in data_list])
longs = np.array([data['LONG'] for data in data_list])
elevations = np.array([data['Elevation_masl'] for data in data_list])
well_depths = np.array([data['Well_depth_m_bgl'] for data in data_list])
depths = elevations - well_depths  # Calculate depth

# Create a new figure for 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each borewell's elevation and depth as connected lines
for i in range(len(data_list)):
    # Extract current well data
    lat = lats[i]
    lon = longs[i]
    elevation = elevations[i]
    depth = depths[i]

    # Create arrays to plot lines from elevation to depth
    xs = [lon, lon]
    ys = [lat, lat]
    zs = [elevation, depth]

    # Plot the line connecting elevation to depth
    ax.plot(xs, ys, zs, marker='o', linestyle='-', label=f'BW_ID {i + 1}' if i == 0 else "", color='b')

# Set labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Meters')
ax.set_title('Elevation and Depth Profile of Borewell Data')

# Add a legend
ax.legend()

# Show plot
plt.show()