import camelot
import tabula
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class PdfConverter:

    @staticmethod
    def extract_tables_to_csv(pdf_path, output_path='tables.csv'):
        tabula.convert_into(pdf_path, output_path, pages='all', stream=True)

    @staticmethod
    def convert_pdf_to_txt(pdf_file):

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()

        device = TextConverter(rsrcmgr, retstr, laparams=laparams)

        #fp = open(pdf_path, 'rb')

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(pdf_file, pagenos, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str

    # convert pdf pdf_file text to string and save as a text_pdf.txt pdf_file
    @staticmethod
    def save_convert_pdf_to_txt():
        content = PdfConverter.convert_pdf_to_txt()
        txt_pdf = open('text_pdf.txt', 'wb')
        txt_pdf.write(content.encode('utf-8'))
        txt_pdf.close()


if __name__ == '__main__':
    print(PdfConverter.convert_pdf_to_txt('../sites/amd/report.pdf'))
