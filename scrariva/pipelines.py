# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from backports import csv
import json
import os
import io

from scrapy.utils.project import get_project_settings


class PortfolioPerformanceCSVWriter(object):
    def __init__(self):
        resource_base_path = get_project_settings().get("RESOURCE_BASE_PATH")
        self.save_file = os.path.join(resource_base_path, "{}_{}_to_{}.csv")
        print("Saving .csv to {}".format(self.save_file))

    def process_item(self, item, spider):
        isin = spider.isin

        reader = csv.reader(io.StringIO(item['csv']), delimiter=';')
        result = []

        next(reader)  # Skip header

        for line in reader:
            if not line:
                continue

            day = line[0]
            value = line[4]
            result.append((day, value))

        min_time = result[0][0]
        max_time = result[-1][0]

        output_filename = self.save_file.format(isin, min_time, max_time)

        with io.open(output_filename, 'w', newline='', encoding='UTF-8') as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(['Datum', 'Kurs'])
            for t in result:
                writer.writerow([t[0], t[1]])
