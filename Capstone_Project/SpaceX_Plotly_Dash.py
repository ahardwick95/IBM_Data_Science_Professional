# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites=spacex_df['Launch Site'].unique()




# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                               
                                    dcc.Dropdown(id='site-dropdown',
                                        options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': launch_sites[0], 'value': launch_sites[0]},
                                        {'label': launch_sites[1], 'value': launch_sites[1]},
                                        {'label': launch_sites[2], 'value': launch_sites[2]},
                                        {'label': launch_sites[3], 'value': launch_sites[3]}
                                        ],
                                        value='ALL',
                                        placeholder="Space X Launch Sites",
                                        searchable=True
                                        ),


                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',min=int(min_payload), max=int(max_payload), step=1000,marks={0: '0',100: '100'},value=[int(min_payload), int(max_payload)]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        launch_success=spacex_df[spacex_df['class'] == 1].reset_index()
        fig = px.pie(launch_success, values='class', 
        names='Launch Site', 
        title='Success-Rate All Sites')
        return fig
    else:
        site_data=spacex_df[spacex_df['Launch Site']==entered_site]
        site_Suc_Fail=site_data['class'].value_counts().reset_index() 
        fig=px.pie(site_Suc_Fail, names='class', values='count', title=f'Total Success vs Failure for site {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(site,payload_range):
    low, high = payload_range
    The_Range = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)

    if site == 'ALL':
        payload_df = spacex_df[The_Range]
    else:
        payload_df = spacex_df[(spacex_df['Launch Site'] == site) & The_Range]

    fig = px.scatter(payload_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation Between Payload and Launch Outcome',
                     labels={'class': 'Launch Outcome'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
