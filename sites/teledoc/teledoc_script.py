import os
import re
import requests
from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import get_csv_row_index, extract_monetary_value


class Teledoc(Script):

    pdf_url = 'https://s21.q4cdn.com/672268105/files/doc_financials/2020/q1/Teladoc-Health-1Q20-Earnings-Web.pdf'

    net_loss_regex = re.compile('Net loss was \\$\\(?[0-9]+\\.[0-9]+\\)? million')
    eps_line_regex = re.compile('Net loss per share')
    eps_value_regex = re.compile('\\$\\([0-9]+\\.[0-9]+')
    cash_flow_regex = re.compile('\\([0-9,]+\\)')

    def __init__(self):
        super().__init__('Telecop')

    def get_report(self):
        response = requests.get(self.pdf_url)

        with open('report.pdf', 'wb') as f:
            f.write(response.content)

        report_file = open('report.pdf', 'rb')
        self.report_text = PdfConverter.convert_pdf_to_txt(report_file)

        report_file.close()
        f.close()

        PdfConverter.extract_tables_to_csv('report.pdf')
        self.table_lines = open('tables.csv').readlines()  # Saved here for efficiency

    def parse_net_income(self):     # Parses value & assigns to value dict
        net_loss_string = self.net_loss_regex.search(self.report_text).group().replace("(", '').replace(')', '')
        self.values[self.NET_INCOME_TAG] = "".join(["-", extract_monetary_value(net_loss_string)])

    def parse_revenue(self):
        rev_index = get_csv_row_index('Subscription Access Fees Revenue', self.table_lines)
        total_rev_row = self.table_lines[rev_index + 3]   # US & International precede total
        total_thousands = total_rev_row.split(",", maxsplit=1)[1].split('","')[0]
        total_millions = int(total_thousands.replace('"', '').replace(",", ''))/1000
        self.values[self.REV_TAG] = ' '.join(["-${:.2f}".format(total_millions), 'million'])

    def parse_cash_flow(self):
        cash_index = get_csv_row_index('Cash flows used in operating activities', self.table_lines)

        for row in self.table_lines[cash_index:]:
            if 'Net loss' in row:
                cf_thousands = self.cash_flow_regex.search(row).group().replace('(', '').replace(')', '').replace(",", '')
                cf_million = "${:.2f}".format(int(cf_thousands)/1000)
                self.values[self.CASH_TAG] = " ".join(["-" + cf_million, 'million'])

    def parse_EPS(self):    # EPS value line may be offset
        report_lines = self.report_text.split("\n")
        for index, line in enumerate(report_lines):
            if self.eps_line_regex.search(line):
                value_index = index
                while True or value_index >= len(report_lines):
                    s = self.eps_value_regex.search(report_lines[value_index])
                    if s:
                        self.values[self.EPS_TAG] = "-" + s.group(0).replace("(", '').replace(")", '')
                        return
                    value_index += 1

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(Teledoc())