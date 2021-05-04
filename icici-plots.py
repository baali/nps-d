import json
import requests
import pandas as pd
from datetime import date

from bokeh.layouts import column
from bokeh.palettes import all_palettes
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
COLORS = all_palettes['Colorblind'][4]
TIERS = [1, 2]

def plot_tier(tier):
    t_plot = figure(
        x_axis_type='datetime',
        title='ICICI Prudential Pension Fund, Tier: {}'.format(tier),
        plot_height=400, plot_width=900,
        tools=['hover,pan,xbox_select,wheel_zoom,reset'],
    )
    t_plot.grid.grid_line_alpha=0.3
    t_plot.xaxis.axis_label = 'Date'
    t_plot.yaxis.axis_label = 'Price'
    for (index, scheme) in enumerate(SCHEMES):
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
                                       'prices': list(prices_column),
                                       'd_str': [entry['x'] for entry in data]})
            t_plot.line(x='dates', y='prices',
                        color=COLORS[index],
                        source=source,
                        legend_label='Scheme: {}'.format(scheme))
            t_plot.legend.title = 'Tier: {}'.format(tier)
            t_plot.legend.location = 'top_left'
            t_plot.hover.tooltips=[
                ('Scheme', scheme),
                ('price', '@prices'),
                ('date', '@d_str')
            ]
    return t_plot

t_plots = list(map(plot_tier, TIERS))

# Save to HTML
output_file('docs/icici.html', title='ICICI Prudential Pension Fund')
save(column(children=t_plots))
