import json
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from scipy.interpolate import griddata

# Initialize the Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Load transformed JSON data
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


# Function to create an interactive 3D plot using Plotly
def create_3d_plot(cluster_label, year):
    lons, lats_filtered, swl_year = [], [], []
    for i in range(len(data_list)):
        if well_clusters[i] != cluster_label:
            continue

        lat = lats[i]
        lon = longs[i]
        swl = None

        if year == 2016:
            swl = elevations[i] - data_list[i]['SWL_2016_mbgl'] if data_list[i]['SWL_2016_mbgl'] is not None and \
                                                                   data_list[i]['SWL_2016_mbgl'] > 0 else None
        elif year == 2017:
            swl = elevations[i] - data_list[i]['SWL_2017_m_bgl'] if data_list[i]['SWL_2017_m_bgl'] is not None and \
                                                                    data_list[i]['SWL_2017_m_bgl'] > 0 else None

        if swl is not None and swl > 0:
            lons.append(lon)
            lats_filtered.append(lat)
            swl_year.append(swl)

    lons, lats_filtered, swl_year = np.array(lons), np.array(lats_filtered), np.array(swl_year)

    # Create grid for interpolation
    grid_lon, grid_lat = np.meshgrid(
        np.linspace(min(longs), max(longs), 50),
        np.linspace(min(lats), max(lats), 50)
    )

    # Interpolate SWL data to grid
    grid_swl = griddata((lons, lats_filtered), swl_year, (grid_lon, grid_lat), method='cubic')

    # Plotly 3D surface plot
    fig = go.Figure(data=[go.Surface(
        z=grid_swl,
        x=grid_lon,
        y=grid_lat,
        colorscale='viridis',
        colorbar=dict(title='SWL (m)')
    )])

    fig.update_layout(
        title=f'SWL {year} - Cluster {cluster_label}',
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='SWL (m)',
            zaxis=dict(range=[min(grid_swl.flatten()), max(grid_swl.flatten())])
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig


# Define Dash layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("SWL 3D Plot Viewer"), className="text-center")
        ]),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='cluster-dropdown',
                options=[
                    {'label': 'Cluster A', 'value': 'A'},
                    {'label': 'Cluster B', 'value': 'B'},
                    {'label': 'Cluster C', 'value': 'C'}
                ],
                value='A'
            ), width=6),
            dbc.Col(dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': '2016', 'value': 2016},
                    {'label': '2017', 'value': 2017}
                ],
                value=2016
            ), width=6)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='plot-container'))
        ])
    ])
])


# Define callback to update plot
@app.callback(
    Output('plot-container', 'figure'),
    [Input('cluster-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_plot(cluster_label, year):
    fig = create_3d_plot(cluster_label, year)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
