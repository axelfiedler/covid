# covid
## Comparison of Dash and Streamlit using a simple Covid-19 app.

The Python libraries Dash by Plotly and Streamlit are compared using the example of a simple Covid-19 app. This example shows how Streamlit can produce powerful data exploration tools with extremely little code. The used data is directly fetched from [Our World in Data](https://ourworldindata.org/coronavirus-source-data).

Using Dash the resulting app looks like this:

<img src="https://github.com/axelfiedler/covid/blob/main/dash_screenshot.PNG" width="200">

In comparison the app using Streamlit looks like this:
<img src="https://github.com/axelfiedler/covid/blob/main/streamlit_screenshot.PNG" width="200">

Both apps feature the same functionality, however Streamlit seems to be significantly slower than Dash. On the other hand the Streamlit only requires roughly half the lines of code of the Dash app. To make the appearance of the Dash app similar, a style sheet is placed in the `assets` folder.
