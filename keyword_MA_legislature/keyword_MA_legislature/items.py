# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KeywordMaLegislatureItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BillItem(scrapy.Item):
    url = scrapy.Field()
    bill_no = scrapy.Field()
    leg_body = scrapy.Field()
    bill_no_int = scrapy.Field()
    session_no = scrapy.Field()
    filed_by = scrapy.Field()
    filed_by_first = scrapy.Field()
    filed_by_middle = scrapy.Field()
    filed_by_last = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    full_text = scrapy.Field()
    full_text_link = scrapy.Field()
