import os
import re

import requests

from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import format_value_millions


class Delta(Script):

    delta_pdf = 'https://s2.q4cdn.com/181345880/files/doc_news/2020/Delta-Air-Lines-Announces-March-Quarter-2020-Financial-Results.pdf'

    net_income_regex = re.compile('Net (\\(loss\\))?[/ ]income')
    eps_regex = re.compile('Diluted (\\(loss\\))?[/ ]?earnings per share')
    rev_regex = re.compile('Operating revenue')

    def __init__(self):
        super().__init__('Delta')

    @staticmethod
    def get_row_with_regex(rows: [], regex: re):
        for row in rows:
            if regex.search(row):
                return row.lower()

    @staticmethod
    def parse_value_from_row(row):
        return row.split(",")[2].replace(")", '').replace('(', '').strip()

    def get_report(self):
        response = requests.get(self.delta_pdf)

        with open('report.pdf', 'wb') as f:
            f.write(response.content)
        f.close()

        report_file = open('report.pdf', 'rb')
        PdfConverter.extract_tables_to_csv('report.pdf')
        self.table_rows = open('tables.csv').readlines()
        report_file.close()

    def parse_net_income(self):
        income_row = self.get_row_with_regex(self.table_rows, self.net_income_regex)
        income_raw = self.parse_value_from_row(income_row)
        self.values[self.NET_INCOME_TAG] = format_value_millions(income_raw, 'loss' in income_row)

    def parse_revenue(self):
        rev_row = self.get_row_with_regex(self.table_rows, self.rev_regex)
        rev_raw = rev_row.split(",", maxsplit=1)[1].split(",,")[0].replace('"', '').strip().replace(",", '')
        self.values[self.REV_TAG] = format_value_millions(rev_raw)

    def parse_cash_flow(self):
        pass    # TODO

    def parse_EPS(self):
        eps_row = self.get_row_with_regex(self.table_rows, self.eps_regex)
        eps_raw = self.parse_value_from_row(eps_row)
        self.values[self.EPS_TAG] = "".join(["-$" if 'loss' in eps_row else "$", eps_raw])

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(Delta())
