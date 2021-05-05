import pandas as pd

from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource

data = pd.read_csv('data/sbi/data.csv', sep='\t')

SCHEMES = ['A', 'C', 'E', 'G']
COLORS = all_palettes['Colorblind'][4]
TIERS = ['I', 'II']

def plot_tier(tier):
    t_plot = figure(
        x_axis_type='datetime',
        title='SBI Pension Fund, Tier: {}'.format(tier),
        plot_height=400, plot_width=900,
        tools=['hover,pan,xbox_select,wheel_zoom,reset'],
    )
    t_plot.grid.grid_line_alpha=0.3
    t_plot.xaxis.axis_label = 'Date'
    t_plot.yaxis.axis_label = 'Price'
    for (index, scheme) in enumerate(SCHEMES):
        fund_code = '{}{}'.format(scheme, tier)
        t_plot.line(x='Date', y='{} Tier {}'.format(scheme, tier),
                    color=COLORS[index],
                    source=ColumnDataSource(data),
                    legend_label='Scheme: {}'.format(scheme))
        t_plot.legend.title = 'Tier: {}'.format(tier)
        t_plot.legend.location = 'top_left'
        t_plot.hover.tooltips=[
            ('Scheme', scheme),
            # ('price', '@prices'),
            ('date', 'Date')
        ]
    return t_plot

t_plots = list(map(plot_tier, TIERS))

# Save to HTML
output_file('docs/sbi.html', title='SBI Pension Fund')
save(column(children=t_plots))
