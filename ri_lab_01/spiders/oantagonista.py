# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from datetime import datetime


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    allowed_domains = ['oantagonista.com']
    start_urls = []
    limit_data = datetime.strptime('01/01/2018', '%d/%m/%Y')

    def __init__(self, *a, **kw):
        super(OantagonistaSpider, self).__init__(*a, **kw)
        with open('seeds/oantagonista.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for new in response.css('div.collect article'):
            data = new.css('a.article_link span.postmeta time::attr(datetime)').get()
            data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            editedData = data.strftime("%d/%m/%Y %H:%M:%S")
            
            if (data >= self.limit_data):
                yield{
                    'titulo':new.css('a.article_link::attr(title)').get(),
                    'subtitulo':'Nao possui',
                    'autor':'Nao possui',
                    'data':editedData,
                    'secao':new.css('a.article_link span.postmeta span.categoria::text').get(),
                    'texto':new.css('a.article_link p').get(),
                    'url':new.css('a.article_link::attr(href)').get()
                }
            else:
                quit()
                
                
        listUrl = response.url.split("/")     #Quando visualizando por página, o número da página fica após a primeira
                                              #barra(direita para esquerda)
                                              # ex: 
                                              #     ['https:', '', 'www.oantagonista.com', 'pagina', '1', '']
        
        if len(listUrl) == 6:
            newPage = listUrl[0] + '//' + listUrl[2] + '/' + listUrl[3] + '/' + str(int(listUrl[4]) + 1) + '/'
        else:
            newPage = listUrl[0] + '//' + listUrl[2] + '/' + 'pagina' + '/' + '2' + '/'
                                          
        yield scrapy.Request(url=newPage, callback=self.parse)    

                   
    
        
                            
                            
                            
                            
                            
                            