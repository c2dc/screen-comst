from urllib.parse import quote
import scrapy

from scrapper.items import FirmwareItem

  

class TplinkSpider(scrapy.Spider):
    name = "tplinkSpider"
    start_urls=['https://www.tp-link.com/br/support/download']

    def parse(self,response):
        base_url = 'https://www.tp-link.com'
        urls = response.xpath('//a[contains(@data-vars-event-category,"Support-Download")]/@href').getall()
        for url in urls:
            yield scrapy.Request(base_url+url,self.parseModel)
            return


    def parseModel(self,response):
        urls = response.xpath('//dl[@class="select-version"]//li/a/@href').getall()
        for url in urls:
            yield scrapy.Request(url,self.parseVersion)
            return


    def parseVersion(self,response):
        firmware = FirmwareItem()
        firmware['vendor'] = "TP-Link"
        firmware['model'] = response.xpath('//em[@id="model-version-name"]/text()').get()
        firmware['version'] = response.xpath('//em[@id="model-version-name"]/span/text()').get()
        urls = response.xpath('//div[@data-id="Firmware"]//a[@class="download-resource-btn ga-click"]/@href').getall()
        #urls = [url.replace(' ',"%20") for url in urls]
        firmware['file_urls'] = urls
        yield firmware