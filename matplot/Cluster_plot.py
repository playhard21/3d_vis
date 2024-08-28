import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib

# Set backend for PyCharm (this ensures the 3D plot shows)
matplotlib.use('TkAgg')

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

# Manual clustering based on depth ranges
well_clusters = []
for depth in well_depths:
    if depth <= 112:
        well_clusters.append('A')  # Cluster A: 0-112 m
    elif 113 <= depth <= 246:
        well_clusters.append('B')  # Cluster B: 113-246 m
    else:
        well_clusters.append('C')  # Cluster C: > 247 m

# Function to interpolate and plot SWL as a surface
def plot_swl_surface(ax, lons, lats, swl, title, cluster_label):
    # Remove invalid (None or zero) SWL values
    valid_indices = np.where((swl > 0) & (swl != None))
    lons, lats, swl = lons[valid_indices], lats[valid_indices], swl[valid_indices]

    # Create grid for interpolation
    grid_lon, grid_lat = np.meshgrid(
        np.linspace(min(longs), max(longs), 50),  # Use global longs
        np.linspace(min(lats), max(lats), 50)     # Use global lats
    )

    # Interpolate SWL data to grid
    grid_swl = griddata((lons, lats), swl, (grid_lon, grid_lat), method='cubic')

    # Plot the interpolated surface
    ax.plot_surface(grid_lon, grid_lat, grid_swl, cmap='viridis', alpha=0.6)
    ax.set_title(f'SWL - {title} (Cluster {cluster_label})')

    # Set z-axis label
    ax.set_zlabel('SWL (m)')

# Function to create and save individual plots for each cluster and year
def plot_swl_cluster(cluster_label, year, save_name):
    # Prepare data for SWL interpolation
    lons, lats_filtered, swl_year = [], [], []
    fractures = []  # Fractures for the wells in the current cluster

    # Extract well data for the specified cluster
    for i in range(len(data_list)):
        if well_clusters[i] != cluster_label:
            continue

        # Extract current well data
        lat = lats[i]
        lon = longs[i]
        swl = None

        # Choose SWL data based on the year
        if year == 2016:
            swl = elevations[i] - data_list[i]['SWL_2016_mbgl'] if data_list[i]['SWL_2016_mbgl'] is not None and data_list[i]['SWL_2016_mbgl'] > 0 else None
        elif year == 2017:
            swl = elevations[i] - data_list[i]['SWL_2017_m_bgl'] if data_list[i]['SWL_2017_m_bgl'] is not None and data_list[i]['SWL_2017_m_bgl'] > 0 else None

        # Append only valid SWL data
        if swl is not None and swl > 0:
            lons.append(lon)
            lats_filtered.append(lat)
            swl_year.append(swl)

    # Convert to numpy arrays
    lons, lats_filtered, swl_year = np.array(lons), np.array(lats_filtered), np.array(swl_year)

    # Create a new figure for SWL plotting
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot interpolated SWL for the given year
    plot_swl_surface(ax, lons, lats_filtered, swl_year, f'SWL {year}', cluster_label)

    # Plot wells as grey cylinders
    for i in range(len(lons)):
        ax.plot([lons[i], lons[i]], [lats_filtered[i], lats_filtered[i]], [elevations[i], depths[i]], color='gray', linewidth=2)

    # Set labels and limits
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('SWL (m)')
    ax.invert_zaxis()
    ax.set_xlim(min(longs), max(longs))
    ax.set_ylim(min(lats), max(lats))
    ax.set_zlim(min(depths), max(elevations))
    ax.view_init(elev=30, azim=120)

    # Save the plot as an image
    plt.savefig(f'{save_name}.png')

    # Show the plot with interactive rotation enabled
    plt.show()

# Generate 6 different plots for each cluster and year combination
plot_swl_cluster('A', 2016, 'Cluster_A_2016_interpolated')
plot_swl_cluster('B', 2016, 'Cluster_B_2016_interpolated')
plot_swl_cluster('C', 2016, 'Cluster_C_2016_interpolated')
plot_swl_cluster('A', 2017, 'Cluster_A_2017_interpolated')
plot_swl_cluster('B', 2017, 'Cluster_B_2017_interpolated')
plot_swl_cluster('C', 2017, 'Cluster_C_2017_interpolated')
