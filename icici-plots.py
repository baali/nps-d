import json
import requests
import pandas as pd
from datetime import date

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource

def fetch_data(fund_code):
    # curl 'https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest?fundCode=C1&startDate=21-NOV-04&endDate=24-APR-21'
    today = '{}-{}-{}'.format(
        date.today().strftime('%d'),
        date.today().strftime('%b').upper(),
        date.today().strftime('%y'))
    icici_inception_date = '18-MAY-2009'
    icici_data = requests.get(
        'https://www.iciciprupensionfund.com/pensionFunds/iprupnsnfunds/navhistory.rest',
        params={'fundCode': fund_code,
                'startDate': icici_inception_date,
                'endDate': today}).json()
    return icici_data

def get_dates(entry):
    return pd.to_datetime(entry['x'])

def get_prices(entry):
    return entry['y']


SCHEMES = ['A', 'C', 'E', 'G']
TIERS = [1, 2]

icici_p = figure(
    x_axis_type='datetime',
    title='ICICI Prudential Pension Fund',
    plot_height=200, plot_width=900,
    tools=['pan,xbox_select,wheel_zoom,reset'])
icici_p.grid.grid_line_alpha=0.3
icici_p.xaxis.axis_label = 'Date'
icici_p.yaxis.axis_label = 'Price'

for tier in TIERS:
    for scheme in SCHEMES:
        fund_code = '{}{}'.format(scheme, tier)
        print('Fetching data for Tier: {} Scheme: {}'.format(tier, scheme))
        try:
            data = fetch_data(fund_code)
        except json.decoder.JSONDecodeError:
            print('No data for Tier: {} Scheme: {}'.format(tier, scheme))
        else:
            dates_column = map(get_dates, data)
            prices_column = map(get_prices, data)
            source = ColumnDataSource({'dates': list(dates_column),
                                       'prices': list(prices_column)})
            icici_p.line(x='dates', y='prices', source=source)

# Save to HTML
output_file('docs/icici.html', title='ICICI Prudential Pension Fund')
save(icici_p)
