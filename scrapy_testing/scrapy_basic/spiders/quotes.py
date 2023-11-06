import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest 

import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2Fjobs%3Fq%3Dauditor&tmpl=desktop&from=gnav-util-jobsearch--indeedmobile&jsContinue=https%3A%2F%2Fwww.indeed.com%2Fjobs%3Fq%3Dauditor&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.166200702.1564862577.1699038730-1320592664.1699038730'

        yield SplashRequest(url, callback=self.parse, args={'proxy': 'http://scrapeops:e744b2eb-d700-4ded-a918-34d17ad2da01@proxy.scrapeops.io:5353' })



    def parse(self, response):
        open_in_browser(response)