import scrapy
from scrapy.crawler import CrawlerProcess
import os
from bs4 import BeautifulSoup
import time


class EksisozSpider(scrapy.Spider):

    name = 'eksisoz'
    def __init__( self , linkk ):
        try:
            os.remove('info.json')
        except:
            pass
        self.page_count = 1
        self.entry_list = []
        self.link = linkk

    def start_requests(self):
        if '?' in self.link:
            link_index = self.link.index('?')
            self.link = self.link[0:link_index]

        urls = [
            self.link
        ]
        yield scrapy.Request(url=self.link, callback=self.parse)


    def parse(self, response):
        entry = response.css('div.content').getall()
        entry_author = response.css('a.entry-author::text').getall()
        entry_time = response.css('a.entry-date.permalink::text').getall()
        entry_author_index = 0
        for i in entry:
            soup = BeautifulSoup(i, 'html.parser')
            i = soup.get_text()
            i = i.replace( '\r\n' , '' )
            i = i.replace('\n', '')
            i = i + ' Author : {} Time : {} '.format(entry_author[entry_author_index] , entry_time[entry_author_index])
            self.entry_list.append(i)
            entry_author_index += 1

        # self.entry_list = []

        all_page_count = response.css( 'div.pager::attr(data-pagecount)' ).get()


        #Sayfalari geziyor
        if int(self.page_count) < int(all_page_count):

            self.page_count = self.page_count + 1
            yield scrapy.Request(url = self.link+'?p={}'.format(self.page_count) , callback = self.parse)
        elif int(self.page_count) == int(all_page_count):
            yield {
                'entry': self.entry_list,
                'entry_count': len(self.entry_list),
            }

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'info.json',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_DEBUG': False
})
def start(a):
    process.crawl(EksisozSpider,linkk = a)
    process.start()




