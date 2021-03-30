# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from amazon_script.spiders.seller_asin import RunSpider
from datetime import datetime
import sys
import xlsxwriter
import xlrd
import os
from threading import Thread
from scrapy.utils.project import get_project_settings

SETTINGS = get_project_settings()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.file1 = ''
        self.file2 = ''
        self.setWindowTitle("Amazon ASINs")
        self.setGeometry(550, 250, 860, 550)
        self.UiComponents()
        self.show()

    def UiComponents(self):

        # creating a label
        self.label = QLabel(self)
        self.label.setText("Enter URL")
        self.label.setGeometry(20, 20, 150, 30)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setFont(QFont('Arial', 15))

        self.input = QLineEdit(self)
        self.input.setGeometry(190, 20, 600, 30)

        self.input1 = QLineEdit(self)
        self.input1.setGeometry(50, 160, 600, 30)

        self.browse_input2 = QLineEdit(self)
        self.browse_input2.setGeometry(50, 220, 600, 30)

        self.browse_input1 = QLineEdit(self)
        self.browse_input1.setGeometry(50, 160, 600, 30)

        self.browse_btn1 = QPushButton("Browse file1", self)
        self.browse_btn1.setGeometry(690, 160, 100, 30)
        self.browse_btn1.clicked.connect(self.browse_file1)

        self.browse_btn2 = QPushButton("Browse file2", self)
        self.browse_btn2.setGeometry(690, 220, 100, 30)
        self.browse_btn2.clicked.connect(self.browse_file2)

        self.get_asin = QPushButton("Get ASINs", self)
        self.get_asin.setGeometry(350, 70, 200, 40)
        self.get_asin.setFont(QFont('Arial', 13))
        self.get_asin.clicked.connect(self.run_spider)

        self.cpmpare = QPushButton("Compare ASINs", self)
        self.cpmpare.setGeometry(350, 270, 200, 40)
        self.cpmpare.setFont(QFont('Arial', 13))
        self.cpmpare.clicked.connect(self.compare_asin)

        self.b = QPlainTextEdit(self)
        self.b.move(5, 335)
        self.b.resize(850, 210)
        self.b.insertPlainText("Details here...\n")

    def browse_file1(self):
        self.file1 = QFileDialog.getOpenFileName(self, 'open file', os.path.abspath(''))
        if self.file1[0].split('.')[1].lower() == 'xlsx':
            self.browse_input1.setText(self.file1[0])
        else:
            QMessageBox.critical(self, "Error", "please select only csv files")

    def browse_file2(self):
        self.file2 = QFileDialog.getOpenFileName(self, 'open file', os.path.abspath(''))
        if self.file2[0].split('.')[1].lower() == 'xlsx':
            self.browse_input2.setText(self.file2[0])
        else:
            QMessageBox.critical(self, "Error", "please select only xlsx files")

    def compare_asin(self):
        asins = []
        dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S").replace('/', '').replace(',', '').replace(' ', '').replace(':', '')
        file_name = 'compared_asin_{}.xlsx'.format(dt)
        path = '{}\{}'.format(os.path.abspath(''), file_name)
        if self.file1 and self.file2:
            workbook = xlrd.open_workbook(self.file1[0])
            worksheet = workbook.sheet_by_index(0)
            workbook1 = xlrd.open_workbook(self.file2[0])
            worksheet1 = workbook1.sheet_by_index(0)

            for y in range(0, worksheet.nrows -1):
                if worksheet.cell_value(y, 0) in asins:
                    continue
                frequency = 0
                for x in range(0, worksheet1.nrows - 1):
                    if worksheet.cell_value(y, 0) == worksheet1.cell_value(x, 0):
                        frequency += 1
                        if frequency == 1:
                            if worksheet.cell_value(y, 0) not in asins:
                                asins.append(worksheet.cell_value(y, 0))
                    if frequency == 0:
                        if worksheet.cell_value(y, 0) not in asins:
                            asins.append(worksheet.cell_value(y, 0))

            new_workbook = xlsxwriter.Workbook(path)
            new_worksheet = new_workbook.add_worksheet()
            for i in range(0, len(asins) - 1):
                new_worksheet.write(i, 0, asins[i])
            new_workbook.close()
            message = "Created New File, File location: {}".format(path)
            self.b.insertPlainText(message)

        else:
            QMessageBox.critical(self, "Error", "Please Select csv files")

    def run_spider(self):
        self.b.insertPlainText("Please wait Script is running, excel file will created after finish scraping."
                               "")
        try:
            url = self.input.text()
        except:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle('Error')
            error_dialog.showMessage('Something Wrong please try agian')
        if url:
            self.get_asin.setEnabled(False)
            run_spider = RunSpider()
            run_spider.run_process(url)
            self.b.insertPlainText("\nFinished Scraping")

        else:
            QMessageBox.critical(self, "Error", "Please Enter the URL")


if __name__ == "__main__":
    # creating thread
    App = QApplication(sys.argv)
    window = Window()
    t1 = Thread(target=sys.exit(App.exec()), args=(10,))


