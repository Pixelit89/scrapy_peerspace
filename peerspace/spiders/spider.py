from scrapy.spiders import CrawlSpider, Request
import requests
from ..items import PeerspaceItem
import re

class PeerSpider(CrawlSpider):
    name = "peer"
    allowed_domains = ['peerspace.com']
    start_urls = ['https://www.peerspace.com/']

    def parse(self, response):
        res = requests.get('https://www.peerspace.com/v1/search/listings?viewport_bbox=[40.95474862138328,-74.22456331933597,40.605869270113715,-73.7260586806641]&space_use=Production&ffilter=web-search&use_subtype=Photo%20Shoot&use_id=photo-shoot')
        total = res.json()['hits']['total']
        json_res = requests.get('https://www.peerspace.com/v1/search/listings?viewport_bbox=[40.95474862138328,-74.22456331933597,40.605869270113715,-73.7260586806641]&space_use=Production&ffilter=web-search&size={}&use_subtype=Photo%20Shoot&use_id=photo-shoot'.format(total))
        data = json_res.json()['hits']['hits']
        for place in data:
            yield Request(url='https://www.peerspace.com/pages/listings/{}'.format(place['_id']), callback=self.parse_saves)

    def parse_saves(self, response):
        item = PeerspaceItem()
        result = re.findall('\(\d+\)', response.xpath('//button[@id="favorites-btn"]/span[1]').extract_first())
        item['link'] = response.url
        item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        item['location'] = '{}, {}'.format(response.xpath('//div[@id="listing-info-block"]/div[@class="row"]/div[1]/p[1]/a/text()').extract_first(), ''.join(response.xpath('//div[@id="listing-info-block"]/div[@class="row"]/div[1]/p[1]/a/span/text()').extract()))
        item['price'] = response.xpath('//div[@class="price"]/text()').extract_first()
        item['about_the_space'] = response.xpath('//p[@class="body-copy-1"]/text()').extract_first()
        try:
            item['saves'] = result[0].decode('utf-8')[1: -1]
        except IndexError:
            item['saves'] = 0
        return item