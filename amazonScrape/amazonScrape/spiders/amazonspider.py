from __future__ import print_function
import scrapy
import os
from time import sleep
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



class AmazonScrape(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = ['https://www.amazon.in/s?k=gaming+mouse']
    download_delay = 5.0

    def parse(self, response):
        self.logger.info(f"String Parse on {response.url}")

        search_results = response.css('div.s-result-list.s-search-results')

        search_row = search_results.css('.s-result-item.s-asin')

        for row in search_row:
            image = row.css('img.s-image').xpath('@src').get()
            name = row.css('img.s-image').xpath('@alt').get()
            price = row.css('span.a-price-whole::text').get()
            rating = row.css('i.a-icon-star-small > span.a-icon-alt::text').get()
            customers_rated = row.css('div.a-size-small span.a-size-base::text').get()
            market_price = row.css('span.a-text-price.a-price > span::text').get()

            yield {
                'name': name,
                'price': price,
                'rating': rating,
                'img': image,
                'customers_rated': customers_rated,
                'market_price': market_price
            }

        # going to next page.
        for a in search_results.css('ul.a-pagination li.a-normal > a'):
            self.logger.info(f"Going to Next page")
            yield response.follow(a, callback=self.parse)