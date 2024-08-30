import trimesh
import numpy as np

# Create function to export data to a 3D mesh format
def export_to_3d_model(lons, lats, swl, cluster_label, year):
    # Create vertices from your longitude, latitude, and SWL data
    vertices = np.column_stack((lons, lats, swl))

    # Generate faces for the mesh (triangulation)
    # Assuming your data points are in a grid, create triangles between points
    faces = []
    rows, cols = 50, 50  # Assuming a 50x50 grid
    for i in range(rows - 1):
        for j in range(cols - 1):
            idx = i * cols + j
            faces.append([idx, idx + 1, idx + cols])
            faces.append([idx + 1, idx + cols + 1, idx + cols])

    faces = np.array(faces)

    # Create the mesh
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Export the mesh to a file format, such as OBJ or GLB
    mesh.export(f'{cluster_label}_{year}.obj')  # Export as OBJ format

    print(f"3D model exported as {cluster_label}_{year}.obj")

# Example data
lons = np.linspace(0, 1, 50)
lats = np.linspace(0, 1, 50)
swl = np.random.random(50)  # Replace with your SWL data

# Use the function to export the model
export_to_3d_model(lons, lats, swl, 'A', 2016)
