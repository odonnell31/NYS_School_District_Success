# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:50:23 2020

@author: ODsLaptop
"""

# import libraries
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# import stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initiate dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'NYS Ed'
# read in data
df = pd.read_csv('data/Merged_dataset/NYS_Education_2019_v3.csv')

# all student kpis
student_kpis = ['Grade 3 ELA', 'Grade 3 Math', 'Grade 4 ELA', 'Grade 4 Math',
       'Grade 5 ELA', 'Grade 5 Math', 'Grade 6 ELA', 'Grade 6 Math',
       'Grade 7 ELA', 'Grade 7 Math', 'Grade 8 ELA', 'Grade 8 Math',
       'Graduation_Rate', 'Regents_Diploma_Rate',
       'Advanced_Regents_Diploma_rate',
       'Dropout_rate']

# all unique school districts
#df['School_district'].unique()

# create dash app layout
app.layout = html.Div([
    html.H4(children='New York State Educational Success vs Teachers Salary by School District (2019)',id='credits'),
    html.H3(children='Choose an education metric from the dropdown, then hover over points:', id='title'),
    html.Div([
            
        # top left dropdown for student success kpi
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in student_kpis],
                value='Graduation_Rate'
            )
            
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        
        # top right dropdown for single school district
        #html.Div([
        #    dcc.Dropdown(
        #        id='crossfilter-school-district',
        #        options=[{'label': i, 'value': i} for i in df['School_district'].unique()],
        #        value='SACHEM CENTRAL SCHOOL DISTRICT'
        #    )
        #], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    # scatter plot
    html.Div([
        dcc.Graph(
            id='crossfilter-scatter',
            hoverData={'points': [{'customdata': 'School_district'}]}
        )
    ], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dash_table.DataTable(id='school-district-table',
                             columns = [{"name": 'School District', "id": 'School_district'},
                                        {"name": 'County', "id": 'County'},
                                        {"name": 'Disctrict Description', "id": 'District_description'},
                                        {"name": 'Students Graduated in 2019', "id": 'Graduation_count'},
                                        {"name": 'Teachers Salary (Median)', "id": 'Median_Teachers_Pay'}])
        #dcc.Textarea(id='school-district-kpi')
        #html.A('Code on Github', href='https://github.com/odonnell31/NYS_Educational_Success'),
        #html.Br(),
        #html.A("Data Source", href='https://data.nysed.gov/downloads.php')
    ], style={'display': 'inline-block', 'width': '90%', 'padding': '0 20'}),

    html.Div([
        html.A('Code on Github', href='https://github.com/odonnell31/NYS_Educational_Success'),
        html.Br(),
        html.A("Data Source", href='https://data.nysed.gov/downloads.php')
        ]
    )



])

@app.callback(
    dash.dependencies.Output('crossfilter-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
     #dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     #dash.dependencies.Input('crossfilter-school-district', 'value')])


def update_graph(yaxis_column_name):
    
    dff = df

    return {
        'data': [dict(
            x = dff['Median_Teachers_Pay'].values,
            y = dff[yaxis_column_name].values,
            text = dff['School_district'],
            customdata = dff['School_district'],
            mode='markers',
            marker={
                'size': 12,
                'opacity': 0.4,
                'line': {'width': 0.5, 'color': 'white'}
            }
            #name = dff['School_district'].values,
            #hover_data = dff['School_district'].values
        )],
        'layout': dict(
            xaxis={
                'title': 'Median Teachers Salary'
            },
            yaxis={
                'title': yaxis_column_name
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 50, 'b': 40, 't': 10, 'r': 0},
            height=400,
            hovermode='closest',
            trendline = 'lowess'
            
        )
    }

@app.callback(
    dash.dependencies.Output('school-district-table', 'data'),
    [dash.dependencies.Input('crossfilter-scatter', 'hoverData')]
)
def update_table(hoverData):
    school_district_hover = hoverData['points'][0]['customdata']
    
    school_district_data = df[df['School_district'] == school_district_hover]

    #soql_url = ('http://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
    #        '$select=health,count(tree_id)' +\
    #        '&$where=boroname=\'' + boro + '\'' +\
    #        '&$group=health').replace(' ', '%20')

    #soql_trees = pd.read_json(soql_url)
    
    #return soql_trees.to_dict('records')
    return school_district_data.to_dict('records')

"""
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
"""

if __name__ == '__main__':
    app.run_server(debug=True)