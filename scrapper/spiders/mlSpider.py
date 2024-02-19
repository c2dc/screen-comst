from socket import VM_SOCKETS_INVALID_VERSION
import scrapy
import math
import re

class Router(scrapy.Item):
    vendor = scrapy.Field()
    model = scrapy.Field()
    reviews = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    sells = scrapy.Field()

class BuscapeSpider(scrapy.Spider):

    name = "mlSpider"
    #start_urls=['https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/#applied_filter_id%3Dcategory%26applied_filter_name%3DCategorias%26applied_filter_order%3D4%26applied_value_id%3DMLB5867%26applied_value_name%3DRoteadores%26applied_value_order%3D11%26applied_value_results%3D87445%26is_custom%3Dfalse']
    start_urls=['https://lista.mercadolivre.com.br/roteador-wifi#trends_tracking_id=dd7a130f-11b4-4821-bd55-3842d687e24b']
    

    def parse(self,response):
        #self.log('ACESSANDO URL: %s' % response.url)
        qtd_pages = response.xpath('//li[@class="andes-pagination__page-count"]/text()').getall()[1]
        
        for i in range(0, int(qtd_pages)):
           #https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/_Desde_{1+(i*48)}_NoIndex_True
           page = f'https://lista.mercadolivre.com.br/informatica/conectividade-redes/roteadores/roteador-wifi_Desde_{1+(i*48)}_NoIndex_True'
           yield scrapy.Request(page,self.parsePages)
        

    def parsePages(self,response):
        print(f'\n\nParsing Page: {response.url}\n')
        routerLinks = response.xpath('//section//ol/li/div/div/div/a/@href').getall()
        for router in routerLinks:
            yield scrapy.Request(router, self.parseRouter)


    def parseRouter(self,response):
        print(f'\n\n-->Parsing Router: {response.url}\n')
        router = Router()
        
        router['url'] = response.url

        vendor = response.xpath("//tbody/tr//td/span/text()").getall()
        if len(vendor) > 1:
            router['vendor'] = vendor[0]
            router['model'] = vendor[1]
        
        sells = response.xpath('//div/span[contains(@class,"subtitle")]/text()').get()
        if len(sells) > 0:
            router['sells'] = sells.split(' ')[4]

        reviews = response.xpath('//span[@class="ui-pdp-review__amount"]/text()').get().split(' ')[0]
        if len(reviews) > 0:
            router['reviews'] = reviews
        
        price = response.xpath('//meta[@itemprop="price"]/@content').get()
        if len(price) > 0:
            router['price'] = price
        
        yield router