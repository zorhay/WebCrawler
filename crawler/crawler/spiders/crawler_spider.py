# python 3
from crawler.items import CrawlerItem

import scrapy
from urllib.parse import urljoin


class CrawlerSpider(scrapy.Spider):
	name = 'crawler'
	start_urls = ['http://չտես.հայ/%D5%8D%D5%BA%D5%A1%D5%BD%D5%A1%D6%80%D5%AF%D5%B8%D5%B2:%D4%B2%D5%B8%D5%AC%D5%B8%D6%80%D5%A7%D5%BB%D5%A5%D6%80%D5%A8',]
	visited_urls = []

	def parse(self, response):
		if response.url not in self.visited_urls:
			self.visited_urls.append(response.url)

			for post_link in response.xpath(
				'//div[@class="post mb-2"]/h2/a/@href').extract():
				url = urljoin(response.url, post_link)
				print(url)

			next_pages = response.xpath(
				'//li[contains(@class, "page-item") and'
				' not(contains(@class, "active"))]/a/@href').extract()
		
			next_page = next_pages[-1] if next_pages != [] else ''

			next_page_url = urljoin(response.url+'/', next_page)
			yield response.follow(next_page_url, callback=self.parse)

	def parse_post(self, response):
		item = CrawlerItem()
		title = response.xpath(
			'//div[contains(@class, "col-sm-9")]/h2/text()').extract()
		item['title'] = title
		body = response.xpath(
			'//div[@class="block-paragraph"]//p/text()').extract()

		item['body'] = body
		date = response.xpath(
			'//div[contains(@class, "col-sm-9")]/p/text()').extract()
		item['date'] = date
		yield item