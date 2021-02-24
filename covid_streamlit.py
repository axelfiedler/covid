# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:43:18 2021

@author: fiedl
"""

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import altair as alt

data = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

data['date']= pd.to_datetime(data['date'])

column = st.selectbox('Select column',['total_cases','total_cases_per_million','total_deaths','total_deaths_per_million'])
countries = st.multiselect('Select countries',data["location"].unique())

country_max_cases = []
country_cases = pd.DataFrame()
for country in countries:
    country_cases = country_cases.append(data[data["location"] == country],ignore_index=True)
    country_max_cases.append(np.max(data[data["location"] == country][column]))

df_max = pd.DataFrame({
  'country': countries,
  column: country_max_cases
})

df_max = df_max.set_index('country',drop=True)

col1, col2 = st.beta_columns(2)

with col1:
    st.bar_chart(df_max)

chart = alt.Chart(country_cases).mark_line().encode(
    x=alt.X('date', axis=alt.Axis(tickCount=10, grid=False)),
    y=alt.Y(column),
    color='location',
    #strokeDash='location',
)

with col2:
    st.altair_chart(chart, use_container_width=True)