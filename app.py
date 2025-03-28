# allow the user to explore the province line graphs 
# Import the packages needed:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
# Provice dataset
filename3 = "province.csv"
ProvD = pd.read_csv(filename3, engine = 'python')

# Define the app layout
app = dash.Dash(__name__)

# create the layout of the application
app.layout = html.Div([
    # title
    html.H1("Insurance Metrics per Province Over the Years"),
    # create the dorpdown meny
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Number of Claimants', 'value': 'Claimants'},
            {'label': 'Cost', 'value': 'Cost'},
            {'label': 'Volume', 'value': 'Volumes'}
        ],
        value='Claimants',
        clearable=False
    ),
    dcc.Graph(id='line-graph')
])

# set the application callback
@app.callback(
    Output('line-graph', 'figure'),
    Input('metric-dropdown', 'value')
) # define the graph
def update_graph(selected_metric):
    df_filtered = ProvD.groupby(["Year", "Province"], as_index=False)[selected_metric].sum() # filter to avoid multiple lines
    fig = px.line( # make the figures
        df_filtered, x="Year", y=selected_metric, color="Province",
        markers=True, title=f"{selected_metric} per Province Over the Years"
    )
    fig.update_layout( # make a legend
        legend=dict(
            title="Province",
            x=1.05,  # Move legend to the right outside the figure
            y=1
        )
    )
    return fig # return the figure

if __name__ == '__main__':
    app.run(debug=True, port = 8085) # my laptop only lets you do app.run not app.run_server for some strange reason
