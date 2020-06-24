import re

import requests

NUMBER_REGEX = re.compile('[0-9]+')
MONEY_REGEX = re.compile('(\\$[0-9]+(\\.[0-9]+)?)+ ?([Bb]illion|[Mm]illion)?')


def extract_monetary_value(txt):
    try:
        return MONEY_REGEX.search(txt).group()
    except Exception as e:
        print("No group found")


def get_csv_row_index(row_flag: str, csv_lines):
    for index, row in enumerate(csv_lines):
        if row_flag in row:
            return index


if __name__ == '__main__':
    s = extract_monetary_value('cash equivalents balance was $246.4')
    print(str(s))