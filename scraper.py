"""Basic scraper for Health Inspection Data from King County."""

from bs4 import BeautifulSoup
import requests
import sys
import re
from pprint import pprint

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}


def load_inspection_page(file_name):
    """Load current html to return BeautifulSoup html object."""
    with open('inspection_page.html', 'rb') as file:
        html = file.read()
    return html, 'utf-8'


def get_inspection_page(**kwargs):
    """Get the inspection html file."""
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    """Get then returns the BeautifulSoup html object."""
    parsed_html = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed_html


def extract_data_listings(html):
    """Return the div of every listing."""
    id_re = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_re)


def has_two_tds(element):
    """
    Return True if the element is both a <tr>.

    And contains exactly two <td> elements immediately within it.
    """
    td_children = element.find_all('td', recursive=False)
    return element.name == 'tr' and len(td_children) == 2


def clean_data(td):
    """Clean data from td and returns it."""
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(element):
    """Extract and return metadata."""
    rows = element.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    data = {}
    current_label = ''
    for row in rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        label = clean_data(key_cell)
        current_label = label if label else current_label
        data.setdefault(current_label, []).append(clean_data(val_cell))
    return data


def is_inspection_row(element):
    """Return True if the element is the inspection row."""
    if not element.name == 'tr':
        return False
    td = element.find_all('td', recursive=False)
    has_four = len(td) == 4
    text = clean_data(td[0]).lower()
    has_word = 'inspection' in text
    return has_four and has_word and not text.startswith('inspection')


def extract_score_data(element):
    """Extract and return score data from listing div."""
    rows = element.find_all(is_inspection_row)
    samples = len(rows)
    total = 0
    high_score = 0
    average = 0
    for row in rows:
        value = clean_data(row.find_all('td')[2])
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += int_value
            high_score = int_value if int_value > high_score else high_score
    if samples:
        average = total / samples
    data = {
        'Average Score': float(average),
        'High Score': high_score,
        'Total Inspections': samples
    }
    return data


if __name__ == '__main__':
    kwargs = {
        'Zip_Code': '98118',
        'Inspection_Start': '3/5/2013',
        'Inspection_End': '8/7/2015'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    parsed_html = parse_source(html, encoding)
    listings = extract_data_listings(parsed_html)
    for listing in listings:
        data = extract_restaurant_metadata(listing)
        data.update(extract_score_data(listing))
        pprint(data)
        print()
    print('Number of listings: ', len(listings))
