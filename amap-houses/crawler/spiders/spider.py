# -*- coding: utf-8 -*-
from re import sub
from scrapy import Spider
from scrapy.http import HtmlResponse
from crawler.items import House

trans_dict = str.maketrans({
    '鑶': '9',
    '閏': '6',
    '餼': '1',
    '驋': '4',
    '鸺': '7',
    '麣': '3',
    '齤': '8',
    '龒': '2',
    '龤': '0',
    '龥': '5'
})


class SpiderSpider(Spider):
    name = 'spider'
    raw_string = 'https://sz.58.com/pinpaigongyu/pn/{page}/?minprice=2000_3000'
    allowed_domains = ['sz.58.com']
    start_urls = ['https://sz.58.com/pinpaigongyu/pn/1/?minprice=2000_3000']

    def parse(self, response: HtmlResponse):
        # 提取房源列表
        house_list = response.xpath(
            '//li[@class="house"]/a/div[2]/h2/text()').getall()
        if not house_list:
            # 没有房源信息则结束
            return
        # 提取URL列表
        url_list = response.xpath('//li[@class="house"]/a/@href').getall()
        # 提取价格列表
        money_list = response.xpath(
            '//li[@class="house"]/a/div[@class="money"]//b/text()').getall()
        for title, url, money in zip(house_list, url_list, money_list):
            title = title.strip().translate(trans_dict)
            info = title.split()
            # 若第2列是公寓名，则首列是地址
            if '公寓' in info[1] or '青年社区' in info[1]:
                location = info[0]
            else:
                location = info[1]
            money = sub(r'\s', '', money).translate(trans_dict)
            # 将数据封装为对象进行返回
            yield House(title=title,
                        location=location.strip().translate(trans_dict),
                        money=money,
                        url=url.strip())
        # 追踪下一个链接
        page_no = int(response.url.split('/')[-2]) + 1
        yield response.follow(self.raw_string.format(page=page_no))
