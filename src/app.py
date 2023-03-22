# imports
from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import altair as alt

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------------------------
# Load the processed data

data = pd.read_csv("../data/processed/data.csv")

# helper functions
def pivot_longer():
    df = data.copy()

    # Data long format
    id_vars = [
        "Date",
        "Price (USD per Barrel)",
        "SLB Price (USD)",
        "SP500 Price (USD)",
        "Month",
        "Year",
    ]
    value_vars = [
        "Canada",
        "Middle East",
        "Asia Pacific",
        "U.S.",
        "Latin America",
        "Europe",
        "Africa",
    ]

    df_long = pd.melt(
        data,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="Location",
        value_name="Rig Count",
    )

    return df_long


def normalize(series):
    series = series.apply(lambda x: (x - series.min()) / (series.max() - series.min()))
    return series


# PLOTS


def plot_normalized_lineplots(year_range):
    # Filtering the dataframe by values passed
    df = data.copy()
    df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

    df_normalized = df[
        ["Date", "Price (USD per Barrel)", "SLB Price (USD)", "SP500 Price (USD)"]
    ]

    df_normalized = df_normalized.assign(
        Oilprice_normalized=normalize(df_normalized["Price (USD per Barrel)"])
    )
    df_normalized = df_normalized.assign(
        SLBprice_normalized=normalize(df_normalized["SLB Price (USD)"])
    )
    df_normalized = df_normalized.assign(
        SP500price_normalized=normalize(df_normalized["SP500 Price (USD)"])
    )

    df_normalized.drop(
        ["Price (USD per Barrel)", "SLB Price (USD)", "SP500 Price (USD)"],
        axis=1,
        inplace=True,
    )

    df_normalized = df_normalized.melt(
        id_vars=["Date"],
        value_vars=[
            "Oilprice_normalized",
            "SLBprice_normalized",
            "SP500price_normalized",
        ],
    )

    plot = (
        alt.Chart(df_normalized)
        .mark_line()
        .encode(
            x="Date:T",
            y="value",
            color="variable:N",
        )
        .properties(width=250, height=300)
    )

    return plot.to_html()


def plot_oilprice_rigcount(year_range):
    # Filtering the dataframe by values passed
    df = data.copy()
    df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

    # Plotting
    plot_oil = (
        alt.Chart(df)
        .mark_line(color="green")
        .encode(
            y=alt.Y(
                "Price (USD per Barrel)",
                axis=alt.Axis(title="Oil Price (USD)", titleColor="green"),
            ),
            x="Date:T",
            tooltip=["Price (USD per Barrel)"],
        )
    )

    plot_rigcount = (
        alt.Chart(df)
        .mark_line(color="red")
        .encode(
            y=alt.Y(
                "Total World",
                axis=alt.Axis(title="Worldwide Rig Count", titleColor="red"),
            ),
            x="Date:T",
            tooltip=["Total World"],
        )
    )

    # Combine the two plots
    plot = (
        alt.layer(plot_oil, plot_rigcount)
        .resolve_scale(y="independent")  # make the y-axes independent
        .properties(width=300, height=300)
    )

    return plot.to_html()


def plot_oilprice_slb(year_range):
    # Filtering the dataframe by values passed
    df = data.copy()
    df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

    # Plotting
    plot_oil = (
        alt.Chart(df)
        .mark_line(color="green")
        .encode(
            y=alt.Y(
                "Price (USD per Barrel)",
                axis=alt.Axis(title="Oil Price (USD)", titleColor="green"),
            ),
            x="Date:T",
            tooltip=["Price (USD per Barrel)"],
        )
    )

    plot_slb = (
        alt.Chart(df)
        .mark_line(color="darkblue")
        .encode(
            y=alt.Y(
                "SLB Price (USD)",
                axis=alt.Axis(title="SLB Stock Price (USD)", titleColor="darkblue"),
            ),
            x="Date:T",
            tooltip=["SLB Price (USD)"],
        )
    )

    # Combine the two plots
    plot = (
        alt.layer(plot_oil, plot_slb)
        .resolve_scale(y="independent")  # make the y-axes independent
        .properties(width=300, height=300)
    )

    return plot.to_html()


# TBD consistent color scheme for stacked bars
def plot_market_rigcount(year_range, market):

    df_long = pivot_longer()

    # Filter be year range
    df_long = df_long[
        (df_long["Year"] >= year_range[0]) & (df_long["Year"] <= year_range[1])
    ]

    # Filter by market
    df_long = df_long[df_long["Location"].isin(market)]

    plot = (
        alt.Chart(df_long)
        .mark_bar()
        .encode(
            y="mean(Rig Count)",
            x="Year:N",
            color="Location",
        )
    ).properties(width=350, height=350)

    return plot.to_html()


# -----------------------------------------
# Layout

h1_style = {"font-size": "42px", "color": "blue", "text-align": "center"}
h2_style = {"font-size": "18px", "color": "black", "text-align": "left"}
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1(
                    "Oil Market Dashboard",
                    style=h1_style,
                )
            ]
        ),
        dbc.Row([html.P("An overview of the Oil Economy", style=h2_style)]),
        html.Br(),
        # Add Widget - Select year range
        dbc.Row(
            [
                "Select Year Range",
                dcc.RangeSlider(
                    min=1986,
                    max=2023,
                    step=None,
                    value=[1986, 2000],
                    marks={
                        1986: "1986",
                        1990: "1990",
                        1995: "1995",
                        2000: "2000",
                        2005: "2005",
                        2010: "2010",
                        2015: "2015",
                        2020: "2020",
                        2023: "2023",
                    },
                    id="select_year_slider",
                ),
            ],
        ),
        html.Br(),
        # Add 3 LinePlots in one row
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Oil price and Rig count Line plot
                        html.Div(
                            [
                                "Oil Price vs Worldwide Rig Count",
                                html.Iframe(
                                    id="oilprice_lineplot",
                                    srcDoc=plot_oilprice_rigcount(
                                        year_range=[1986, 2000]
                                    ),
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        # Oil price vs SLB stock price
                        html.Div(
                            [
                                "Oil Price vs SLB Stock price",
                                html.Iframe(
                                    id="oilprice_slb_lineplot",
                                    srcDoc=plot_oilprice_slb(year_range=[1986, 2000]),
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        # Normalized lineplots
                        html.Div(
                            [
                                "Normalized Price comparison",
                                html.Iframe(
                                    id="normalized_lineplots",
                                    srcDoc=plot_normalized_lineplots(
                                        year_range=[1986, 2000]
                                    ),
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        # Add the checklists
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([html.P("Select Region")]),
                        html.Div(
                            [
                                dcc.Checklist(
                                    id="market_checklist",
                                    options=[
                                        {"label": "Africa", "value": "Africa"},
                                        {
                                            "label": "Asia Pacific",
                                            "value": "Asia Pacific",
                                        },
                                        {"label": "Canada", "value": "Canada"},
                                        {"label": "Europe", "value": "Europe"},
                                        {
                                            "label": "Latin America",
                                            "value": "Latin America",
                                        },
                                        {
                                            "label": "Middle East",
                                            "value": "Middle East",
                                        },
                                        {"label": "United States", "value": "U.S."},
                                    ],
                                    value=["U.S."],
                                    labelStyle={
                                        "display": "block",
                                        "cursor": "pointer",
                                        "margin-left": "20px",
                                    },
                                ),
                            ],
                            style={"padding-top": "1px"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        # Market bar plot
                        html.Div(
                            [
                                "Stacked Barplot of Rig Count by Region",
                                html.Iframe(
                                    id="market_rigcount_stackedbars",
                                    srcDoc=plot_market_rigcount(
                                        year_range=[1986, 2000], market=["U.S."]
                                    ),
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),
    ],
    fluid=True,
)


# all callbacks
@app.callback(
    Output("oilprice_lineplot", "srcDoc"),  # Output(id , argument)
    Input("select_year_slider", "value"),  # Input(id , argument)
)
def update_oilprice_rigcount(year_range):
    return plot_oilprice_rigcount(year_range)


@app.callback(
    Output("oilprice_slb_lineplot", "srcDoc"),  # Output(id , argument)
    Input("select_year_slider", "value"),  # Input(id , argument)
)
def update_oilprice_slb(year_range):
    return plot_oilprice_slb(year_range)


@app.callback(
    Output("market_rigcount_stackedbars", "srcDoc"),  # Output(id , argument)
    Input("select_year_slider", "value"),  # Input(id , argument)
    Input("market_checklist", "value"),  # Input(id , argument)
)
def update_market_rigcount(year_range, market):
    return plot_market_rigcount(year_range, market)


@app.callback(
    Output("normalized_lineplots", "srcDoc"),  # Output(id , argument)
    Input("select_year_slider", "value"),  # Input(id , argument)
)
def update_normalized_lineplots(year_range):
    return plot_normalized_lineplots(year_range)


server = app.server
