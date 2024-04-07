# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os
import numpy as np
# Read the airline data into pandas dataframe
#path = r'C:\local_data\COURSERA\IBM_applied-data-science-capstone'
#spacex_df = pd.read_csv(path + os.sep+"spacex_launch_dash.csv")
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

launch_list = np.unique(spacex_df['Launch Site'])
launch_options=[{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_list:
    launch_options.append({'label': site, 'value': site})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=launch_options,
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')                                     
                                ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                     min = min_payload,
                                     max = max_payload,
                                     value =[min_payload,max_payload/2]
                                
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
                                
                                
                                
                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def update_successPieChart(input_site):
    pie_title = "Successful launches count for %s"%input_site
    pie_df = pd.DataFrame()
    if input_site == 'ALL':
        pie_df = spacex_df.groupby('class')['Flight Number'].count().reset_index()
    else:
        pie_df = spacex_df[(spacex_df["Launch Site"]==input_site)].groupby('class')['Flight Number'].count().reset_index()
        
    print(pie_df)
    pie_df['class'] = pie_df['class'].map(lambda x:  'Success' if x==1 else 'Fail')
    pie_fig = px.pie(pie_df, names='class',values='Flight Number', title=pie_title )
    #pie_fig.update_traces(hoverinfo='label+percent', textinfo='value')    
    return pie_fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')] )
    
def update_payloadScatterChart(input_site,payloadRange):
    print('--------------------------')
    print(payloadRange)
    title = "Correlation between payload and launch success for %s"%input_site
    showdf = spacex_df
    if input_site != 'ALL':
        showdf = spacex_df[(spacex_df["Launch Site"]==input_site)]
     
    showdf = showdf[((showdf["Payload Mass (kg)"] >= payloadRange[0] )& (showdf["Payload Mass (kg)"] <= payloadRange[1] ))]
    
    fig = px.scatter(showdf, x='Payload Mass (kg)',y='class', title=title,color="Booster Version Category" )
    
    return fig

# Run the app
if __name__ == '__main__':
    
    app.run_server()
