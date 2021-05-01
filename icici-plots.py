import requests
import pandas as pd
from datetime import date

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource

today = '{}-{}-{}'.format(
    date.today().strftime('%d'),
    date.today().strftime('%b').upper(),
    date.today().strftime('%y'))

icici_inception_date = '18-MAY-2009'

# curl 'https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest?fundCode=C1&startDate=21-NOV-04&endDate=24-APR-21' | jq > data/icici/icici-tier-1-scheme-c.json
icici_data = requests.get(
    'https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest',
    params={'fundCode': 'C1',
            'startDate': icici_inception_date,
            'endDate': today}).json()

def get_dates(entry):
    return pd.to_datetime(entry['x'])

def get_prices(entry):
    return entry['y']

dates_column = map(get_dates, icici_data)
prices_column = map(get_prices, icici_data)

source = ColumnDataSource({'dates': list(dates_column),
                           'prices': list(prices_column)})
# Plot the figure
icici_p = figure(
    x_axis_type='datetime',
    title='ICICI Prudential Pension Fund: Scheme:{}/Tier:{}'.format('C', 1),
    plot_height=200, plot_width=900,
    tools=['pan,reset,wheel_zoom'])
icici_p.grid.grid_line_alpha=0.3
icici_p.xaxis.axis_label = 'Date'
icici_p.yaxis.axis_label = 'Price'
icici_p.line(x='dates', y='prices', source=source)

# Save to HTML
output_file('docs/icici.html', title='ICICI Prudential Pension Fund')
save(icici_p)
