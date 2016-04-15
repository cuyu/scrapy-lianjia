#-*- coding:utf-8 -*-
'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 4/13/16
'''

import scrapy
import time
from scrapy_lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "http://sh.lianjia.com/ershoufang"
    ]

    def parse(self, response):
        self.logger.info('Start parsing {0}'.format(response.url))
        for house_info in response.xpath("//ul[@id='house-lst']/li"):
            url = response.urljoin(house_info.xpath("div/a/@href").extract()[0])
            yield scrapy.Request(url, callback=self.parse_house_info)

        next_page_href = response.xpath("//div[@class='page-box house-lst-page-box']/a/@href").extract()[-1]
        is_on_last_page = response.xpath("//div[@class='page-box house-lst-page-box']/a")[-1].xpath("@class")
        if not is_on_last_page:
            url = response.urljoin(next_page_href)
            yield scrapy.Request(url, self.parse)

    def parse_house_info(self, response):
        self.logger.info('Start parsing {0}'.format(response.url))
        # FIXME: Use more graceful method to handle the redirect issue.
        # Sleep some time to work around the `anti-crawl` mechanism.
        time.sleep(2)
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

        # Extract details in the table.
        sel_table = response.xpath("//table[@class='aroundInfo']/tr")
        sel_table_detail = sel_table.xpath("td/text()")
        item_list = []
        for i in range(7):
            tmp_str = sel_table_detail[i*2+1].extract().strip()
            item_list.append(tmp_str)
        item['price_per_area'], item['floor_number'], item['year'], item['decoration'], item['direction'], item['first_pay'], item['month_pay'] = item_list
        # Extract community.
        item['community'] = sel_table[-2].xpath("td/a/text()").extract()[0]
        # Extract district.
        tmp_str = sel_table[-2].xpath("td/text()").extract()[1]
        tmp_str = tmp_str.replace(r'（'.decode('utf-8'),'')
        tmp_str = tmp_str.replace(r'）'.decode('utf-8'),'')
        item['district'] = tmp_str
        # Extract address.
        item['address'] = sel_table[-1].xpath("td/p/text()").extract()[0]
        yield item
