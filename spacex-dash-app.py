# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'}
                 ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder='Select a Launch Site here',
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Pie chart
    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    # TASK 3: Range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload]),

    # TASK 4: Scatter plot
    dcc.Graph(id='success-payload-scatter-chart'),
])

# TASK 2 callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(selected_site):
    filtered_df = spacex_df
    if selected_site == 'ALL':
        fig = px.pie(filtered_df,
                     values='class',
                     names='Launch Site',
                     title='Total Success Launches for All Sites')
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        site_df = site_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(site_df,
                     values='count',
                     names='class',
                     title=f'Total Success vs Failure for {selected_site}')
    return fig

# TASK 4 callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def scatter(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        fig = px.scatter(df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Payload vs Success for All Sites')
    else:
        site_df = df[df['Launch Site'] == selected_site]
        fig = px.scatter(site_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
