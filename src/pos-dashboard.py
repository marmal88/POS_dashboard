import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv(
    "data/WebAssignment.csv",
    parse_dates={"Date": ["YYYY", "MM", "DD"]},
    keep_date_col=True,
)
df["Revenue"] = df[
    "Amount"
]  # According to Meta Data "The Unit Price of this product sales multiply by Quantity"
df["Profit"] = df["Revenue"] - df["Cost"]
df["Year"] = df["YYYY"].astype("string")  # Created Year as string for graphs
df["YYYY"] = df["YYYY"].astype("int64")  # For range slider min max value
yearlist = {
    x: x for x in range(min(df["YYYY"]), max(df["YYYY"]) + 1)
}  # For range slider mark values
df["MM"] = df["MM"].astype("int64")
df["CustomerPrefix"] = df["CustomerID"].str[:2]
finmetrics = ["Profit", "Cost", "Revenue", "Quantity"]


app = dash.Dash(name='pos-dashboard', external_stylesheets=[dbc.themes.MINTY])
# ----------------------------------
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Dashboard Analysis for Web Assignment", className="card-title"
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H6(
                    "To ensure optimal display, please ensure all "
                    "interactive elements have at least 1 option chosen",
                    className="mb-4",
                ),
                width=12,
            )
        ),
        # Revenue Slider And Bar Graph
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Overall Financial Metrics By Year",
                            className="mb-4"),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Please Select Date Range"),
                        dcc.RangeSlider(
                            id="rangeslider1",
                            value=[2011, 2020],
                            marks=yearlist,
                            min=min(df["YYYY"]),
                            max=max(df["YYYY"]),
                            step=1,
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(
                    [
                        html.H6("Please Select Financial Metric",
                                className="mb-4"),
                        dcc.Dropdown(
                            id="dropdown4",
                            value="Profit",
                            options=[{"label": x, "value": x}
                                     for x in finmetrics],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col([dcc.Graph(id="graph1")], width=12),
            ],
            justify="around",
        ),
        # Customer Segmentation Graph By Payment Type
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Compare Product Performance Over Time",
                            className="mb-4"),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Please Select Date Range"),
                        dcc.RangeSlider(
                            id="rangeslider2",
                            value=[2011, 2020],
                            marks=yearlist,
                            min=min(df["YYYY"]),
                            max=max(df["YYYY"]),
                            step=1,
                        ),
                    ],
                    width=12,
                )
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Please Select Financial Metric",
                                className="mb-4"),
                        dcc.Dropdown(
                            id="dropdown3",
                            value="Profit",
                            options=[{"label": x, "value": x}
                                     for x in finmetrics],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H6("Please Select Payment Type",
                                className="mb-4"),
                        dcc.Dropdown(
                            id="dropdown1",
                            value="Credit",
                            options=[
                                {"label": x, "value": x} for x in df["Type"].unique()
                            ],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H6("Please Select ProductID", className="mb-4"),
                        dcc.Dropdown(id="dropdown2", multi=True),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="graph2"),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Compare Customer Buying Behavior",
                            className="mb-4"),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Please Select Customer Prefix"),
                        dcc.Dropdown(
                            id="dropdown5",
                            multi=True,
                            value=["CA"],
                            options=[
                                {"label": x, "value": x}
                                for x in df["CustomerPrefix"].str.upper().unique()
                            ],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H6("Please Select Customer"),
                        dcc.Dropdown(id="dropdown6", multi=True),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H6("Please Select Year"),
                        dcc.Dropdown(
                            id="dropdown7",
                            value=[x for x in range(2011, 2022)],
                            options=[
                                {"label": x, "value": x}
                                for x in sorted(df["YYYY"].unique())
                            ],
                            multi=True,
                        ),
                    ],
                    width=6,
                ),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="graph3")], width=6),
                dbc.Col([dcc.Graph(id="graph4")], width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="graph5")], width=6),
                dbc.Col([dcc.Graph(id="graph6")], width=6),
            ]
        ),
    ]
)
# ----------------------------------
# Callback for financial metrics by year


@app.callback(
    Output(component_id="graph1", component_property="figure"),
    Input(component_id="rangeslider1", component_property="value"),
    Input(component_id="dropdown4", component_property="value"),
)
def updategraph1(year, finmetric):
    df1 = df[(df["YYYY"] >= year[0]) & (df["YYYY"] <= year[1])]
    df1 = df1.groupby(["Year", "Type"], as_index=False)[
        finmetric].sum().round()
    barplt = px.bar(
        df1, x="Year", y=finmetric, title=f"Total {finmetric} in {year[0]}-{year[1]}"
    )
    return barplt


# Callback for for Selected Product Performance Comparison
# dropdown1 to dependent dropdown2
@app.callback(
    Output("dropdown2", "options"),
    Input("dropdown1", "value"),
)
def drop1todrop2(val1):
    df2 = df[df["Type"] == val1]
    return [{"label": x, "value": x} for x in sorted(df2["ProductID"].unique())]


# Populate for dependant dropdown2
@app.callback(Output("dropdown2", "value"), Input("dropdown2", "options"))
def popdropdown2(availableoptions):
    return availableoptions[0]["value"]


# Barchart
@app.callback(
    Output("graph2", "figure"),
    Input("rangeslider2", "value"),
    Input("dropdown1", "value"),
    Input("dropdown2", "value"),
    Input("dropdown3", "value"),
)
def updategraph2(year, type, productid, finmetrics):
    df3 = df[(df["YYYY"] >= year[0]) & (df["YYYY"] <= year[1])]
    if isinstance(productid, int):
        df3 = df3[(df3["Type"] == type) & (df3["ProductID"] == productid)]
    else:
        df3 = df3[
            (df3["Type"] == type) & (
                df3["ProductID"].isin([int(x) for x in productid]))
        ]
    df3 = df3.groupby(["Year", "Type"], as_index=False)[
        finmetrics].mean().round()
    fig1 = px.bar(df3, x="Year", y=finmetrics, color=finmetrics)
    return fig1


# Call Back for Selected Customer Buying Behaviour
@app.callback(Output("dropdown6", "options"), Input("dropdown5", "value"))
def drop1todrop2(prefixval):
    if isinstance(prefixval, str):
        df5 = df[df["CustomerPrefix"] == prefixval]
    else:
        df5 = df[df["CustomerPrefix"].isin(prefixval)]
    return [{"label": x, "value": x} for x in df5["CustomerID"].str.upper().unique()]


# Populate for dependant
@app.callback(Output("dropdown6", "value"), Input("dropdown6", "options"))
def popdropdown2(availableoptions1):
    print(availableoptions1[0]["value"])
    return availableoptions1[0]["value"]


# Graph
@app.callback(
    Output("graph3", "figure"), Input(
        "dropdown6", "value"), Input("dropdown7", "value")
)
def updategraph3(cust, year):
    if isinstance(cust, str):
        df4 = df[(df["CustomerID"] == cust) & (df["YYYY"].isin(year))]
    else:
        df4 = df[(df["CustomerID"].isin(cust)) & (df["YYYY"].isin(year))]
    df4 = (
        df4.groupby(["YYYY", "CustomerID", "Type"], as_index=False)["Quantity"]
        .mean()
        .round()
    )
    fig3 = px.bar(
        df4,
        x="Quantity",
        y="CustomerID",
        orientation="h",
        hover_name="YYYY",
        color="Type",
    )
    fig3 = fig3.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    return fig3


@app.callback(
    Output("graph4", "figure"), Input(
        "dropdown6", "value"), Input("dropdown7", "value")
)
def updategraph3(cust, year):
    if isinstance(cust, str):
        df4 = df[(df["CustomerID"] == cust) & (df["YYYY"].isin(year))]
    else:
        df4 = df[(df["CustomerID"].isin(cust)) & (df["YYYY"].isin(year))]
    df4 = (
        df4.groupby(["YYYY", "CustomerID", "Type"], as_index=False)["Profit"]
        .mean()
        .round()
    )
    fig4 = px.bar(
        df4,
        x="Profit",
        y="CustomerID",
        orientation="h",
        hover_name="YYYY",
        color="Type",
    )
    fig4 = fig4.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    return fig4


@app.callback(
    Output("graph5", "figure"), Input(
        "dropdown6", "value"), Input("dropdown7", "value")
)
def updategraph3(cust, year):
    if isinstance(cust, str):
        df4 = df[(df["CustomerID"] == cust) & (df["YYYY"].isin(year))]
    else:
        df4 = df[(df["CustomerID"].isin(cust)) & (df["YYYY"].isin(year))]
    df4 = (
        df4.groupby(["YYYY", "CustomerID", "Type"], as_index=False)["Revenue"]
        .mean()
        .round()
    )
    fig5 = px.bar(
        df4,
        x="Revenue",
        y="CustomerID",
        orientation="h",
        hover_name="YYYY",
        color="Type",
    )
    fig5 = fig5.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    return fig5


@app.callback(
    Output("graph6", "figure"), Input(
        "dropdown6", "value"), Input("dropdown7", "value")
)
def updategraph3(cust, year):
    if isinstance(cust, str):
        df4 = df[(df["CustomerID"] == cust) & (df["YYYY"].isin(year))]
    else:
        df4 = df[(df["CustomerID"].isin(cust)) & (df["YYYY"].isin(year))]
    df4 = (
        df4.groupby(["YYYY", "CustomerID", "Type"], as_index=False)["Cost"]
        .mean()
        .round()
    )
    fig6 = px.bar(
        df4, x="Cost", y="CustomerID", orientation="h", hover_name="YYYY", color="Type"
    )
    fig6 = fig6.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    return fig6


# ----------------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
