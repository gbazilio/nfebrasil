import re

from lxml import html


def sanitize(raw_string):
    return re.sub(' +',
                  ' ',
                  raw_string
                  .strip()
                  .replace('\n', ' ')
                  .replace('\xa0', ' '))


def assert_valid_html_string(html_string, parser=html):
    try:
        parser.fromstring(html_string)
    except Exception:
        raise ValueError('Malformed HTML. Impossible to parse.')


def remove_duplicate_entries(list):
    return [dict(item) for item in
            set([tuple(list_item.items())
                 for list_item in list])]

