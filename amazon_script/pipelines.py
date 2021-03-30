# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlsxwriter
import os
from datetime import datetime


class AmazonScriptPipeline:
    def __init__(self):
        self.new_workbook = None
        self.new_worksheet = None
        self.path = None
        self.count = 0

    def open_spider(self, spider):
        dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S").replace('/', '').replace(',', '').replace(' ', '').replace(
            ':', '')
        file_name = 'amazin_asin_{}.xlsx'.format(dt)
        self.path = '{}\{}'.format(os.path.abspath(''), file_name)
        self.new_workbook = xlsxwriter.Workbook(self.path)
        self.new_worksheet = self.new_workbook.add_worksheet()

    def process_item(self, item, spider):
        self.new_worksheet.write(self.count, 0, item['ASIN'])
        self.count += 1
        return item

    def close_spider(self, spider):
        self.new_workbook.close()
