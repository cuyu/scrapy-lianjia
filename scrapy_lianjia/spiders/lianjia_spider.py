'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 4/13/16
'''

import scrapy

from scrapy_lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "http://sh.lianjia.com/ershoufang"
    ]

    def parse(self, response):
        for house_info in response.xpath("//ul[@id='house-lst']/li"):
            url = response.urljoin(house_info.xpath("div/a/@href").extract()[0])
            yield scrapy.Request(url, callback=self.parse_house_info)

    def parse_house_info(self, response):
        sel_houseinfo = response.css("body > div.esf-top > div.cj-cun > div.content > div.houseInfo")
        item = LianjiaItem()
        item['price'] = sel_houseinfo.css("div.price > div").extract()
        item['room'] = sel_houseinfo.css("div.room > div").extract()
        item['area'] = sel_houseinfo.css('div.area > div').extract()
        yield item
