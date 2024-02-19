import scrapy
import math
import re

class Router(scrapy.Item):
    vendor = scrapy.Field()
    model = scrapy.Field()
    reviews = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()

class BuscapeSpider(scrapy.Spider):

    name = "buscapeSpider"
    start_urls=['https://www.buscape.com.br/modem-e-roteador/']
    

    def parse(self,response):
        #self.log('ACESSANDO URL: %s' % response.url)
        r = response.xpath('//div/span/text()[re:test(.,".*resultados.*")]').get()
        qtd_itens = r[:r.find(' ')]
        qtd_pages = math.ceil(int(qtd_itens)/36)
        
        for i in range(1, qtd_pages+1):
           page = f'https://www.buscape.com.br/modem-e-roteador?page={i}'
           yield scrapy.Request(page,self.parsePages)
        yield scrapy.Request("https://www.buscape.com.br/modem-e-roteador?page=1",self.parsePages)

    def parsePages(self,response):
        routerLinks = response.xpath('//span[contains(@class,"Cell_Cell")]/a/@href').getall()
        for router in routerLinks:
            if "www" not in router:
                yield scrapy.Request(self.start_urls[0]+router, self.parseRouter)


    def parseRouter(self,response):
        
        router = Router()
        router['url'] = response.url

        #Se tem ficha técnica:
        if response.xpath("//table/tbody/tr").get() is not None: 
            router['vendor'] = response.xpath("//table/tbody//tr/td/a/@title").getall()[0]
            router['model'] = response.xpath("//table/tbody//td/span/text()").get()
        else:
            #Será necessário tratar posteriormente
            router['model'] = response.xpath("//h1/text()").get()
        
        reviews = response.xpath('//a[contains(@href,"avaliacao-dos-usuarios")]/span/text()').get()
        if (reviews is not None):
            reviews = reviews[reviews.find('(')+1:]
            router['reviews'] = re.search("\d+",reviews).group()

        router['price'] = response.xpath('//strong/text()').get()

        yield router
