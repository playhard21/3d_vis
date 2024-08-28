import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

# Set interactive backend for PyCharm (this enables rotation)
matplotlib.use('Qt5Agg')

# Function to load the transformed JSON data
def load_transformed_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Load the transformed data
data_list = load_transformed_json('C:/Users/Gassmann/PycharmProjects/3d_vis/matplot/transformed_data.json')

# Extract and prepare data for plotting
lats = np.array([data['LAT'] for data in data_list])
longs = np.array([data['LONG'] for data in data_list])
elevations = np.array([data['Elevation_masl'] for data in data_list])
well_depths = np.array([data['Well_depth_m_bgl'] for data in data_list])
depths = elevations - well_depths  # Calculate depth

# New data fields to extract with handling for None values
casing_depths = np.array([
    elevations[i] - data['Casing_end_m_bgl'] if data['Casing_end_m_bgl'] is not None else elevations[i]
    for i, data in enumerate(data_list)
])
swl_2016 = np.array([
    elevations[i] - data['SWL_2016_mbgl'] if data['SWL_2016_mbgl'] is not None else elevations[i]
    for i, data in enumerate(data_list)
])
swl_2017 = np.array([
    elevations[i] - data['SWL_2017_m_bgl'] if data['SWL_2017_m_bgl'] is not None else elevations[i]
    for i, data in enumerate(data_list)
])

# Helper function to plot a circle (ring) at a specific depth
def plot_circle(ax, lon, lat, depth, radius, color, label=''):
    # Define circle parameters
    theta = np.linspace(0, 2 * np.pi, 100)
    x = lon + radius * np.cos(theta)
    y = lat + radius * np.sin(theta)
    z = np.full_like(x, depth)
    ax.plot(x, y, z, color=color, label=label)

# Create a new figure for 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each borewell's elevation and depth as pipes with internal circles for SWL and fractures
for i in range(len(data_list)):
    # Extract current well data
    lat = lats[i]
    lon = longs[i]
    elevation = elevations[i]
    depth = depths[i]
    casing_depth = casing_depths[i]
    swl16 = swl_2016[i]
    swl17 = swl_2017[i]

    # Plot the "pipe" from elevation to depth
    ax.plot([lon, lon], [lat, lat], [elevation, depth], color='gray', linestyle='-', linewidth=4)

    # Plot casing depth as a line within the pipe
    ax.plot([lon, lon], [lat, lat], [elevation, casing_depth], color='black', linestyle='-', linewidth=2, label='Casing Depth' if i == 0 else "")

    # Plot SWL 2016 and SWL 2017 as circles within the well cylinder
    plot_circle(ax, lon, lat, swl16, 0.0002, 'blue', 'SWL 2016' if i == 0 else "")
    plot_circle(ax, lon, lat, swl17, 0.0002, 'darkblue', 'SWL 2017' if i == 0 else "")

    # Plot dry fractures as brown circles within the pipe
    for j, fracture_depth in enumerate(data_list[i]['Dry_Fractures']):
        fracture_elevation = elevation - fracture_depth
        plot_circle(ax, lon, lat, fracture_elevation, 0.0002, 'brown', 'Dry Fractures' if i == 0 and j == 0 else "")

    # Plot yielding fractures as green circles within the pipe
    for j, fracture_depth in enumerate(data_list[i]['Yielding_Fractures']):
        fracture_elevation = elevation - fracture_depth
        plot_circle(ax, lon, lat, fracture_elevation, 0.0002, 'green', 'Yielding Fractures' if i == 0 and j == 0 else "")

# Set labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Meters')
ax.set_title('3D Borewell Profile with Casing, SWL, and Fractures')

# Invert the Z-axis to flip the borewell depth visualization
ax.invert_zaxis()

# Reduce the number of latitude and longitude ticks (markers)
ax.set_xticks(np.linspace(min(longs), max(longs), 5))  # Fewer longitude markers
ax.set_yticks(np.linspace(min(lats), max(lats), 5))    # Fewer latitude markers

# Remove the grid for cleaner visual output
ax.grid(False)

# Set axis limits to make the plot look cubic
ax.set_xlim(min(longs), max(longs))
ax.set_ylim(min(lats), max(lats))
ax.set_zlim(min(depths), max(elevations))

# Set initial viewing angle
ax.view_init(elev=30, azim=120)

# Add a legend
ax.legend()

# Show plot with interactive rotation enabled
plt.show()
