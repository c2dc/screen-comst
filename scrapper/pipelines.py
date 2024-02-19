# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from urllib import response
from scrapy.pipelines.files import FilesPipeline
import scrapy
from itemadapter import ItemAdapter
import requests


class ScrapperPipeline(FilesPipeline):
    
    def process_item(self, item, spider):

            #path = "/content/drive/firmwares" + item['vendor']

            #for url in item['file_urls']:
            #    print(f'\n\nProcessing{url}')
            #    response = requests.get(url)
            #    open(url[url.rindex('/')+1:len(url)], "wb").write(response.content)
            return item

    
        


