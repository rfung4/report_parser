import os
import re

import requests

from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import format_value_millions


class Boeing(Script):
    pdf_url = 'https://s2.q4cdn.com/661678649/files/doc_financials/quarterly/2020/q1/1Q20-Press-Release.pdf'

    eps_regex = re.compile('Earnings Per Share')
    rev_regex = re.compile('Revenues')
    cf_regex = re.compile('Operating Cash Flow')
    income_regex = re.compile('Earnings From Operations')

    def __init__(self):
        super().__init__('Boeing')

    @staticmethod
    def get_row_with_regex(rows: [], regex: re):
        for row in rows:
            if regex.search(row):
                return row.lower()

    @staticmethod
    def extract_value_from_row(row):
        return row.split(",", maxsplit=1)[1].split()[0].replace('"', '').replace(',', '').strip()\
            .replace(")", '').replace("(", '').replace("$", '')

    def get_report(self):
        response = requests.get(self.pdf_url)
        with open('report.pdf', 'wb') as f:
            f.write(response.content)
        f.close()

        report_file = open('report.pdf', 'rb')
        PdfConverter.extract_tables_to_csv('report.pdf')
        self.table_rows = open('tables.csv').readlines()
        report_file.close()

    def parse_net_income(self):
        income_row = self.get_row_with_regex(self.table_rows, self.income_regex)
        self.values[self.NET_INCOME_TAG] = format_value_millions(self.extract_value_from_row(income_row), 'loss' in income_row)

    def parse_revenue(self):
        rev_row = self.get_row_with_regex(self.table_rows, self.rev_regex)
        self.values[self.REV_TAG] = format_value_millions(self.extract_value_from_row(rev_row))

    def parse_cash_flow(self):
        cf_row = self.get_row_with_regex(self.table_rows, self.cf_regex)
        self.values[self.CASH_TAG] = format_value_millions(self.extract_value_from_row(cf_row), 'loss' in cf_row)

    def parse_EPS(self):
        eps_row = self.get_row_with_regex(self.table_rows, self.eps_regex)
        self.values[self.EPS_TAG] = "".join(["-$" if 'loss' in eps_row else '$', self.extract_value_from_row(eps_row)])

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(Boeing())