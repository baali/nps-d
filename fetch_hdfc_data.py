from requests_html import HTMLSession
import pandas as pd


def fetch_todays_nav():
    NAV_URL = 'https://www.hdfcpension.com/about-hdfc-pmc/nav/'
    session = HTMLSession()
    r = session.get(NAV_URL)
    vals = []
    for span in r.html.find('span'):
        if 'class' in span.attrs and 'numberleft' in span.attrs['class']:
            vals.append(span.text)
    return vals
