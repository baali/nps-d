import requests
import pandas as pd
from datetime import date
from bokeh.sampledata.iris import flowers

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool

icici_p = figure(title = "ICICI Prudential Pension Fund", plot_height=500, plot_width=500, tools=["pan,reset,wheel_zoom"])

today = '{}-{}-{}'.format(
    date.today().strftime('%d'),
    date.today().strftime('%b').upper(),
    date.today().strftime('%y'))

icici_inception_date = '18-MAY-2009'

# curl "https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest?fundCode=C1&startDate=21-NOV-04&endDate=24-APR-21" | jq > data/icici/icici-tier-1-scheme-c.json
icici_data = requests.get(
    "https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest",
    params={"fundCode": "C1",
            "startDate": icici_inception_date,
            "endDate": today}).json()

df = pd.DataFrame(icici_data)
df.rename(columns={'x': 'date', 'y': 'price'})

# Plot the figure
icici_p = figure(x_axis_type="datetime", title="Stock Closing Prices")
icici_p.grid.grid_line_alpha=0.3
icici_p.xaxis.axis_label = 'Date'
icici_p.yaxis.axis_label = 'Price'
icici_p.line("date", "price", color='#A6CEE3', legend_label='Scheme C Tier 1', source=ColumnDataSource(df))

# Save to HTML
output_file("docs/icici.html", title="ICICI Prudential Pension Fund")
save(icici_p)
