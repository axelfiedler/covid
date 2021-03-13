# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 21:45:15 2021

@author: fiedl
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
data=data[~data.iso_code.str.contains("OWID")].fillna(0)

max_cases_per_million = [max(data[data["location"]==location]["total_cases_per_million"]) for location in data["location"].unique()]


map_fig = go.Figure(data=go.Choropleth(
    locations = data['iso_code'].unique(),
    z = max_cases_per_million,
    text = data['location'].unique(),
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Total cases per million',
    selectedpoints = []
))

map_fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0))

country_options = [{'label': country, 'value': country} for country in data["location"].unique()]

app.layout = html.Div([
                html.Div("Select column:"),
                dcc.Dropdown(
                    id='column-dropdown',
                    options=[
                        {'label': "Total cases", 'value': "total_cases"},
                        {'label': "Total cases per million", 'value': "total_cases_per_million"},
                        {'label': "Total deaths", 'value': "total_deaths"},
                        {'label': "Total deaths per million", 'value': "total_deaths_per_million"}],
                    value="total_cases"
                ),
                html.Div("Select countries:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    multi=True
                ),
                dcc.Graph(
                    id="map-graph",
                    figure=map_fig
                ),
                dcc.Graph(
                    id="overview-graph",
                    figure=go.Figure()
                ),
                dcc.Graph(
                    id="line-graph",
                    figure=go.Figure()
                )
            ],id="content")


    

@app.callback(
    [dash.dependencies.Output("overview-graph", 'figure'),
     dash.dependencies.Output("line-graph", 'figure')],
    [dash.dependencies.Input('column-dropdown', 'value'),
     dash.dependencies.Input('map-graph','selectedData'),
     dash.dependencies.Input('country-dropdown','value')
     ])
def update_output(column,selected_points,selected_dropdown):
    selected_countries = []
    if selected_dropdown:
        for option in selected_dropdown:
            selected_countries.append(option)
    if selected_points:
        for point in selected_points["points"]:
            selected_countries.append(point["text"])
    if selected_countries:
        country_max_cases = []
        line_fig = go.Figure()
        for country in selected_countries:
            country_max_cases.append(np.max(data[data["location"] == country][column]))
            line_fig.add_trace(
                go.Scatter(x=data[data["location"] == country]["date"],
                           y=data[data["location"] == country][column],
                           name=country
                )
            )
        overview_fig = go.Figure(data=go.Bar(x=selected_countries,y=country_max_cases))
        overview_fig.update_layout(yaxis_title=column)
        line_fig.update_layout(yaxis_title=column)
    else:
        overview_fig = go.Figure()
        line_fig = go.Figure()
    return overview_fig, line_fig

if __name__ == '__main__':
    app.run_server(debug=True)