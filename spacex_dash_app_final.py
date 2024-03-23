#SpaceX Launches Dashboard
import dash
from dash.dependencies import Input, Output
from dash import dcc,html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()

launch_sites = df['Launch Site'].unique()

app = dash.Dash(__name__)

options_list = [{'label':'All Sites','value':'All Sites'}] + [{'label':site,'value':site} for site in launch_sites]

app.layout = html.Div([html.H1('SpaceX Launch Records Dashboard',style={'text-align':'center','color':'#503D36','font-size':'40'}),
                      html.Div(dcc.Dropdown(id='site-dropdown',
                                            options=options_list,
                                            placeholder='Select launch site',
                                            value='All Sites',
                                            style={'width':'100%','padding':'3px','text-align-last':'center'})),
                        html.Br(),
                        html.Div(dcc.Graph(id='success-pie-chart')),
                        html.P('Payload Range (Kg):'),
                        html.Div(dcc.RangeSlider(id='payload-range-slider',
                                                 min=0,
                                                 max=max_payload,
                                                 step=100,
                                                 value=[0, max_payload],
                                                 marks={2500:'2500',5000:'5000',7500:'7500',10000:'10000',12500:'12500',int(max_payload):str(max_payload)})),
                        html.Div(dcc.Graph(id='payload-chart'))
                      ])

@app.callback([Output(component_id='success-pie-chart',component_property='figure'),
               Output(component_id='payload-chart',component_property='figure')],
              [Input(component_id='site-dropdown',component_property='value'),
               Input(component_id='payload-range-slider',component_property='value')])

def update_graphs(site,payload_range):

    if site=='All Sites':
        success_data = df[df['class']==1].groupby('Launch Site')['class'].sum().reset_index()
        success_pie_chart = px.pie(data_frame=success_data,values='class',names='Launch Site',title='Total Successful Launches by Site')
        payload_chart = px.scatter(df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation between Payload and Success for all Sites')
        payload_chart.update_xaxes(range=payload_range)
        return [success_pie_chart,payload_chart]
    else:
        success_data = df[df['Launch Site']==site].groupby('class').size()
        success_pie_chart = px.pie(values=success_data,names=['Failure','Success'],title='Successful Launches at {}'.format(site))
        payload_chart = px.scatter(df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation between Payload and Success for all Sites')
        payload_chart.update_xaxes(range=payload_range)
        return [success_pie_chart,payload_chart]

if __name__=='__main__':
    app.run_server(debug=True)