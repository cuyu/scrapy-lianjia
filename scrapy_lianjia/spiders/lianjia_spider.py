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

        next_page_href = response.xpath("//div[@class='page-box house-lst-page-box']/a/@href").extract()[-1]
        is_on_last_page = response.xpath("//div[@class='page-box house-lst-page-box']/a")[-1].xpath("@class")
        if not is_on_last_page:
            url = response.urljoin(next_page_href)
            yield scrapy.Request(url, self.parse)

    def parse_house_info(self, response):
        sel_houseinfo = response.xpath("//div[@class='houseInfo']")
        item = LianjiaItem()
        item['url'] = response.url
        item['price'] = sel_houseinfo.xpath("div[@class='price']/div/text()").extract()[0] + \
                        sel_houseinfo.xpath("div[@class='price']/div/span/text()").extract()[0]
        room_info = ''
        room_num = sel_houseinfo.xpath("div[@class='room']/div/text()").extract()
        room_unit = sel_houseinfo.xpath("div[@class='room']/div/span/text()").extract()
        for i in range(len(room_num)):
            room_info += room_num[i] + room_unit[i]
        item['room'] = room_info
        item['area'] = sel_houseinfo.xpath("div[@class='area']/div/text()").extract()[0] + \
                       sel_houseinfo.xpath("div[@class='area']/div/span/text()").extract()[0]
        yield item
