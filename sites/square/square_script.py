import os
import re

import requests
from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import extract_monetary_value


class Square(Script):

    PDF_URL = 'https://s21.q4cdn.com/114365585/files/doc_financials/2019/q4/2019-Q4-Shareholder-Letter-Square.pdf'
    eps_regex = re.compile('Net Income Per Share \\(Adjusted EPS\\) was \\$[0-9]+\\.[0-9]+')

    cash_flow_regex = re.compile('We ended the (first|second|third|fourth) quarter of 20[0-9]{2} with \\$[0-9]+\\.[0-9]+ billion in cash')

    def __init__(self):
        super().__init__('Square')

    def get_report(self):
        response = requests.get(self.PDF_URL)

        with open('report.pdf', 'wb') as f:
            f.write(response.content)
        f.close()

        report_file = open('report.pdf', 'rb')
        PdfConverter.extract_tables_to_csv('report.pdf')
        self.report_text = PdfConverter.convert_pdf_to_txt(report_file).replace("\n", ' ').replace('  ', ' ')
        report_file.close()

    def parse_net_income(self):  # Parsed with rev
        pass

    def parse_revenue(self):
        header_found = False

        for row in open('tables.csv'):
            if header_found:
                value_row = row.split(",")
                rev_val, income_val = value_row[0], value_row[1].split("%")[1]
                self.values[self.REV_TAG] = extract_monetary_value(rev_val).lower()
                self.values[self.NET_INCOME_TAG] = extract_monetary_value(income_val).lower()
                return

            if 'TOTAL NET REVENUE' in row:
                header_found = True

    def parse_cash_flow(self):
        cf = self.cash_flow_regex.search(self.report_text).group()
        self.values[self.CASH_TAG] = extract_monetary_value(cf)

    def parse_EPS(self):
        eps = self.eps_regex.search(self.report_text).group()
        self.values[self.EPS_TAG] = extract_monetary_value(eps)

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(Square())

