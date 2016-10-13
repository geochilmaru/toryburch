# -*- coding: utf-8 -*-

import scrapy
import sys
# import re
from scrapy.spiders import CrawlSpider
from toryburch.items import ToryburchItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

reload(sys)
sys.setdefaultencoding('utf-8')


class TorySpider(CrawlSpider):
    name = "toryburch"
    allowed_domains = ["toryburch.com"]
    start_urls = [
        "http://www.toryburch.com/on/demandware.store/Sites-ToryBurch_US-Site/default/Home-EUShopUS?cid=tb-geo-go-usa"
        ]

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     # Rule(LinkExtractor(allow=('', ), deny=('.*\.html.*', )), callback='parse_detail', follow = True),
    #
    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=(r'-\w+.html$', )),
    #          callback = 'parse_tory', follow = True),
    # )

    # def start_requests(self):
    #     # yield scrapy.Request("http://www.toryburch.com/on/demandware.store/Sites-ToryBurch_US-Site/default/Home-EUShopUS?cid=tb-geo-go-usa", self.parse)
    #     yield scrapy.Request("http://www.coachoutlet.com/", self.parse_coach)

    def parse(self, response):
        hxs = Selector(response)
        categories = ['New Arrivals', 'Baby Bags', 'Backpacks'
            , 'Clutches & Evening Bags', 'Cross-Body Bags', 'Hobos'
            , 'Mini Bags', 'Satchels & Shoulder Bags', 'Totes', 'Sale']
        selects = []
        selects = hxs.xpath('//li[@class="handbags"]/ul/li/ul/li')
        for sel in selects:
            cate_name = sel.xpath('a/@title').extract()
            if categories.count(cate_name[0]) > 0:
                cate_url = sel.xpath('a/@href').extract()
                yield Request(cate_url[0], callback=self.parse_list)

    def parse_list(self, response):
        hxs = Selector(response)
        selects = []
        selects = hxs.xpath('//ol[@typeof="BreadcrumbList"]/li/a/span/text()').extract()
        cate = [sel.encode('utf-8') for sel in selects]
        category = selects.pop()

        del selects[:]
        selects = hxs.xpath('//ol[@typeof="BreadcrumbList"]/li/a/@href').extract()
        category_url = selects.pop()

        del selects[:]
        selects = hxs.xpath('//div[@class="producttile-inner"]')
        items = []
        # p = re.compile(r"^[+-]?\d*(\.?\d*)$")
        for sel in selects:
            item = ToryburchItem()
            name = sel.xpath('div[@class="name"]/a/text()').extract()
            full_name = sel.xpath('div[@class="name"]/a/@title').extract()
            standard_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="discountprice"]/div[@class="standardprice"]/text()').extract()
            sales_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="discountprice"]/div[@class="salesprice"]/text()').extract()
            no_sales_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="salesprice"]/text()').extract()
            desc = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="product-image-primary"]/@title').extract()
            url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/@href').extract()
            img_url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="product-image-primary"]/@src').extract()
            alt_img_url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="alternateimage"]/@src').extract()
            alt_img_desc = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="alternateimage"]/@alt').extract()
            if not standard_price:
                standard_price = no_sales_price
            if not sales_price:
                sales_price = ['$0',]
            item["category"] = category
            item["category_url"] = category_url
            item["name"] = name
            item["full_name"] = full_name
            item["standard_price"] = standard_price
            item["sales_price"] = sales_price
            item["desc"] = desc
            item["url"] = url
            item["img_url"] = img_url
            item["alt_img_url"] = alt_img_url
            item["alt_img_desc"] = alt_img_desc
            yield Request(url[0], callback=self.parse_detail, meta={"item":item})
        #     # items.append(item)
        # # return items


    def parse_detail(self, response):
        item = response.meta['item']
        hxs = Selector(response)
        selects = []
        selects = hxs.xpath('//ul[@class="swatchesdisplay"]/li')
        color = []
        for sel in selects:
            col_attr = {}
            col = sel.xpath('a/span/text()').extract()
            url = sel.xpath('a/@name').extract()
            img_url = sel.xpath('a/img[@class="swatchimage"]/@src').extract()
            col_code = sel.xpath('div/text()').extract()
            col_attr["color"] = col[0].upper()
            col_attr["url"] = url[0]
            col_attr["img_url"] = img_url[0]
            col_attr["col_code"] = col_code[0]
            color.append(col_attr)
        item["color"] = color

        del selects[:]
        selects = hxs.xpath('//div[@class="detailsPanel"]/div/ul')
        detail = []
        for sel in selects:
            lists = sel.xpath('li/text()').extract()
            # dtls = str(dtl.encode('utf-8'))
            dtl = [x.encode('utf-8') for x in lists]
            dtls = "<br>".join(dtl)
            detail.append(dtls)
        details = "<br>".join(detail)
        item["details"] = details
        yield item