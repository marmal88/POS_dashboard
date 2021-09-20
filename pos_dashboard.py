'''
Analysis Goals
1) Compare Financial Metrics By Year
Provide users with an overview over the entire business performance over time.
Why: Business performance metrics are important for management to obtain a helicopter view over the business that they
are managing. Using these performance metrics, management can decide on business strategies going forward.

2) Compare Product Performance
Provide users the ability to explore specific SKU/ProductID and their payment terms.
Why: As the business in question is a trading business, choosing the right products and upselling products is important.
Management must understand which products are most popular over time and which have faded in popularity. This allows
them to make decisions on inventory and product substitution.

3) Compare Customer Buying Behavior
Provide users the ability to explore customer buying behaviour, which customers are recurring vs once off and which have
an increasing requirement for more stock.
Why: Management must have an idea which customers to invest into. A growing customer can be provided with (but not
limited to) priority access to new stock, delivery timeframes, favourable credit terms. This the business to work with
growing partners and thus increase organic sales.
'''

import pandas as pd
import dash
import dash_bootstrap_components as dbc # please pip install dash-bootstrap-components
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('WebAssignment.csv', parse_dates={'Date':['YYYY','MM','DD']}, keep_date_col=True)
df['Revenue'] = df['Amount']    # According to Meta Data "The Unit Price of this product sales multiply by Quantity"
df['Profit'] = df['Revenue'] - df['Cost']
df['Year'] = df['YYYY'].astype('string')    # Created Year as string for graphs
df['YYYY'] = df['YYYY'].astype('int64')     # For range slider min max value
yearlist = {x: x for x in range(min(df['YYYY']), max(df['YYYY'])+1)} # For range slider mark values
df['MM'] = df['MM'].astype('int64')
df['CustomerPrefix'] = df['CustomerID'].str[:2]
finmetrics = ['Quantity', 'Revenue', 'Profit', 'Cost']
# print(df.head())
# print(df.info())


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
#----------------------------------
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Dashboard Analysis for Web Assignment", className='card-title'), width=12)
    ),
    dbc.Row(
        dbc.Col(html.H6("To ensure optimal display, please ensure all "
                        "interactive elements have at least 1 option chosen", className='mb-4'), width=12)
    ),
    # Revenue Slider And Bar Graph
    dbc.Row([
        dbc.Col(html.H4("Overall Financial Metrics By Year", className='mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H6("Please Select Date Range"),
            dcc.RangeSlider(id='rangeslider1', value=[2011,2020], marks=yearlist,
                            min=min(df['YYYY']), max=max(df['YYYY']), step=1),
        ], width=9),
        dbc.Col([
            html.H6("Please Select Financial Metric", className='mb-4'),
            dcc.Dropdown(id='dropdown4', value='Profit', options=[{'label': x,'value':x} for x in finmetrics])
        ], width=3),
        dbc.Col([
            dcc.Graph(id='graph1')
        ])
    ], justify='around'),
    # Customer Segmentation Graph By Payment Type
    dbc.Row([
        dbc.Col(html.H4("Compare Product Performance Over Time", className='mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H6("Please Select Date Range"),
            dcc.RangeSlider(id='rangeslider2', value=[2011,2020], marks=yearlist,
                            min=min(df['YYYY']), max=max(df['YYYY']), step=1),
        ], width=12)
    ], justify='around'),
    dbc.Row([
        dbc.Col([
            html.H6("Please Select Financial Metric", className='mb-4'),
            dcc.Dropdown(id='dropdown3', value='Profit', options=[{'label': x,'value':x} for x in finmetrics])
        ], width=3),
        dbc.Col([
            html.H6("Please Select Payment Type", className='mb-4'),
            dcc.Dropdown(id='dropdown1', value='Credit', options=[{'label':x,'value':x} for x in df['Type'].unique()])
        ], width=3),
        dbc.Col([
            html.H6("Please Select ProductID", className='mb-4'),
            dcc.Dropdown(id='dropdown2', multi=True)
        ], width=6),
        dbc.Col([
            dcc.Graph(id='graph2'),
        ]),
    ]),
    dbc.Row([
        dbc.Col(html.H4("Compare Customer Buying Behavior", className='mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H6("Please Select Customer Prefix"),
            dcc.Dropdown(id='dropdown5', multi=True,
                         options=[{'label':x,'value':x} for x in df['CustomerPrefix'].str.upper().unique()])
        ],width=4),
        dbc.Col([
            html.H6("Please Select Customer"),
            dcc.Dropdown(id='dropdown6', multi=True, value=10002)
        ],width=4),
        dbc.Col([
            html.H6("Please Select Year"),
            dcc.Dropdown(id='dropdown7', value=[x for x in range(2011,2022)],
                         options=[{'label': x,'value':x} for x in sorted(df['YYYY'].unique())], multi=True)
        ],width=4)
    ], justify='around'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph3')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='graph4')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph5')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='graph6')
        ], width=6)
    ])
])
#----------------------------------
# Callback for financial metrics by year
@app.callback(
    Output('graph1', 'figure'),
    Input('rangeslider1', 'value'),
    Input('dropdown4', 'value')
)
def updategraph1(year, finmetric):
    df1 = df[(df['YYYY']>=year[0]) & (df['YYYY']<=year[1])]
    df1 = df1.groupby(['Year','Type'], as_index=False)[finmetric].sum().round()
    barplt = px.bar(df1, x="Year", y=finmetric, title=f'Total {finmetric} in {year[0]}-{year[1]}')
    return barplt

# Callback for for Selected Product Performance Comparison
# dropdown1 to dependent dropdown2
@app.callback(
    Output('dropdown2', 'options'),
    Input('dropdown1', 'value'),
)
def drop1todrop2(val1):
    df2 = df[df['Type']==val1]
    return [{'label':x,'value':x} for x in sorted(df2['ProductID'].unique())]

# Populate for dependant dropdown2
@app.callback(
    Output('dropdown2', 'value'),
    Input('dropdown2', 'options')
)
def popdropdown2(availableoptions):
    return availableoptions[0]['value']

# Barchart
@app.callback(
    Output('graph2', 'figure'),
    Input('rangeslider2', 'value'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('dropdown3', 'value')
)
def updategraph2(year, type, productid, finmetrics):
    df3 = df[(df['YYYY'] >= year[0]) & (df['YYYY'] <= year[1])]
    df3 = df3[(df3['Type']==type) & (df3['ProductID'].isin([int(x) for x in productid]))]
    df3 = df3.groupby(['Year','Type'], as_index=False)[finmetrics].mean().round()
    fig1 = px.bar(df3, x="Year", y=finmetrics, color=finmetrics)
    return fig1

# Call Back for Selected Customer Buying Behaviour
@app.callback(
    Output('dropdown6', 'options'),
    Input('dropdown5', 'value')
)
def drop1todrop2(val1):
    df5 = df[df['CustomerPrefix'].isin(val1)]
    return [{'label':x,'value':x} for x in df5['CustomerID'].str.upper().unique()]

# Populate for dependant
@app.callback(
    Output('dropdown6', 'value'),
    Input('dropdown6', 'options')
)
def popdropdown2(availableoptions1):
    return availableoptions1[0]['value']
# Graph
@app.callback(
    Output('graph3', 'figure'),
    Input('dropdown6', 'value'),
    Input('dropdown7', 'value')
)
def updategraph3(cust, year):
    df4 = df[(df['CustomerID'].isin(cust) & df['YYYY'].isin(year))]
    df4 = df4.groupby(['YYYY','CustomerID','Type'], as_index=False)['Quantity'].mean().round()
    fig2 = px.bar(df4, x='Quantity', y='CustomerID', orientation='h', hover_name='YYYY', color='Type')
    fig2 = fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    return fig2

@app.callback(
    Output('graph4', 'figure'),
    Input('dropdown6', 'value'),
    Input('dropdown7', 'value')
)
def updategraph3(cust, year):
    df4 = df[(df['CustomerID'].isin(cust) & df['YYYY'].isin(year))]
    df4 = df4.groupby(['YYYY','CustomerID','Type'], as_index=False)['Profit'].mean().round()
    fig3 = px.bar(df4, x='Profit', y='CustomerID', orientation='h', hover_name='YYYY', color='Type')
    fig3 = fig3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    return fig3

@app.callback(
    Output('graph5', 'figure'),
    Input('dropdown6', 'value'),
    Input('dropdown7', 'value')
)
def updategraph3(cust, year):
    df4 = df[(df['CustomerID'].isin(cust) & df['YYYY'].isin(year))]
    df4 = df4.groupby(['YYYY','CustomerID','Type'], as_index=False)['Revenue'].mean().round()
    fig3 = px.bar(df4, x='Revenue', y='CustomerID', orientation='h', hover_name='YYYY', color='Type')
    fig3 = fig3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    return fig3

@app.callback(
    Output('graph6', 'figure'),
    Input('dropdown6', 'value'),
    Input('dropdown7', 'value')
)
def updategraph3(cust, year):
    df4 = df[(df['CustomerID'].isin(cust) & df['YYYY'].isin(year))]
    df4 = df4.groupby(['YYYY','CustomerID','Type'], as_index=False)['Cost'].mean().round()
    fig3 = px.bar(df4, x='Cost', y='CustomerID', orientation='h', hover_name='YYYY', color='Type')
    fig3 = fig3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    return fig3


#----------------------------------
if __name__=='__main__':
    app.run_server(debug=False)

'''
Insights from Data
1) Among the financial metrics available, the yearly profit is highly correlated to the yearly amount of quantity sold. 
While it might be easy for management to surmise that to increase profit they must increase volume of trading, I would 
like to offer an alternative insight. Taking the year 2018 as an example, 2018 was a record profitable year for the 
company. However, the company also had to move 20% more products to achieve only a 6% increase in profit vs the previous 
year. The company would be better off focusing on products that have higher margin rather than to increase sales volume.

2) Cash on delivery customers only form a small fraction (<4%) of the overall sales for the business. Depending on the
terms of credit provided and bad debt accrued, A high number of customers on credit may pose a risk to the business. 
As business would be quite affected if a slowdown occurs and customers are unable to make payments on time. 
Management should review the list of customers who are on overly generous payment terms and tighten credit control. 

3) Assuming customer prefix was grouped together by business relationships (i.e. subsidiaries of business provided with 
the same starting prefix). The top 20 customers make up 80% of overall profit over the past 11 years. 
Similarly, the top 2% of products sold accounted for ~50% of the overall profit of the business over the past 11 years. 
As we have no idea of network effects of holding so many inventory items, perhaps management can do a study on which
items are more sought after by their customer and rationalize number of inventory item types.

'''
