import scrapy

from keyword_MA_legislature.items import BillItem


class KeywordSpiderSpider(scrapy.Spider):
    name = "keyword_spider"
    allowed_domains = ["malegislature.gov"]
    start_urls = ["https://malegislature.gov/Bills/Search?SearchTerms=Nurse&Page=1"]

    custom_settings = {
        'FEEDS': {
            'nurse_keyword_data.csv': {'format': 'csv', 'overwrite': True},
        }
    }

    def parse(self, response):

        bills = response.xpath("//table[@id='searchTable']//tbody/tr")

        for bill in bills:

            relative_url = bill.css('td a::attr(href)').get()
            bill_url = "https://malegislature.gov" + relative_url

            yield response.follow(bill_url, callback=self.parse_bill_page)

    def parse_bill_page(self, response):
        bill_no = response.css('h1 ::text').get()
        session_no = response.css('h1 .subTitle ::text').get()

        bill_item = BillItem()

        bill_item['url'] = response.url
        bill_item['bill_no'] = bill_no
        bill_item['session_no'] = session_no
        bill_item['filed_by'] = response.css('div .content dd a ::text').get()
        bill_item['title'] = response.css('div .content h2 ::text').get()
        bill_item['description'] = response.css('div .content p ::text').get()

        yield bill_item
