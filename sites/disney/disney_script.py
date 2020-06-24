import os

import requests

from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import get_csv_row_index
import camelot


class Disney(Script):
    pdf_url = 'https://thewaltdisneycompany.com/app/uploads/2020/05/q2-fy20-earnings.pdf'

    def __init__(self):
        super().__init__('Disney')

    def get_report(self):
        response = requests.get(self.pdf_url)

        with open('report.pdf', 'wb') as f:
            f.write(response.content)
        f.close()

        report_file = open('report.pdf', 'rb')
        t = camelot.read_pdf('report.pdf', pages='1', flavor='stream') # Couldn't use tabula here
        t[0].to_csv('tables.csv')

        self.report_text = PdfConverter.convert_pdf_to_txt(report_file)
        self.table_rows = open('tables.csv').readlines()
        report_file.close()

    @staticmethod
    def parse_value_from_csv(label, table_rows, same_row=True):
        row = table_rows[get_csv_row_index(label, table_rows)] if same_row else\
            table_rows[get_csv_row_index(label, table_rows)+1]
        return row.split(",", maxsplit=2)[-1].split(',"$",')[0].replace('"', '')

    def parse_net_income(self):     # Parses value & assigns to value dict
        net_income_raw = self.parse_value_from_csv('Net income from continuing', self.table_rows, False)
        self.values[self.NET_INCOME_TAG] = "".join(['$', net_income_raw.replace(",", ''), ' million'])

    def parse_revenue(self):
        rev_millions_raw = self.parse_value_from_csv('Revenues', self.table_rows)
        self.values[self.REV_TAG] = "".join(['$', rev_millions_raw.replace(",", ''), ' million'])

    def parse_cash_flow(self):
        cash_flow_raw = self.parse_value_from_csv('Free cash flow', self.table_rows)
        self.values[self.CASH_TAG] = "".join(['$', cash_flow_raw.replace(",", ''), ' million'])

    def parse_EPS(self):
        raw_eps = self.parse_value_from_csv('Diluted EPS', self.table_rows, False)
        self.values[self.EPS_TAG] = "".join(['$', raw_eps])

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(Disney())

