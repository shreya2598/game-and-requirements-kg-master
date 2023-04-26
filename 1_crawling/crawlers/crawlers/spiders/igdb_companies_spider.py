import scrapy
from datetime import datetime

class IGDBCompaniesSpider(scrapy.Spider):
    name = "igdb_companies"
    max_count = -1

    start_urls = ["https://www.igdb.com/companies?page=1"]

    def __init__(self):
        self.cur_count=0

    def parse(self, response):
        # Company page links: response.css("td a::attr(href)").getall()
        # Next page link: response.css("li.next a::attr(href)").get()

        # Follow the company page links:
        for href in response.css("td a::attr(href)"):
            self.cur_count = self.cur_count + 1
            if self.max_count!=-1 and self.cur_count >= self.max_count:
                return
            yield response.follow(href, self.parse_company_page)

        # Follow next page links:
        for href in response.css("li.next a::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_company_page(self, response):
        # Name: response.xpath('//h1/span[contains(@itemprop,"name")]/text()').get()
        # Rating Value: response.xpath('//h1/span[contains(@itemprop,"ratingValue")]/text()').get()
        # Best Rating: 100
        # Number of Ratings: response.xpath('//h1/span[contains(@itemprop,"ratingCount")]/text()').get()

        # Logo: response.css("img.logo_med::attr(src)").get()
        # Website: response.xpath('//div/a[contains(@itemprop,"sameAs")]/@href').get()
        # Founding date: response.xpath('//div[contains(@itemprop,"foundingDate")]/time/@datetime').get()
        # Country: response.xpath('//div[contains(@itemprop,"foundingLocation")]/text()').get()

        # Extract all the attributes of the company:
        cur_url = str(response.url)
        cur_timestamp = str(datetime.utcnow())
        cur_company_name = response.xpath('//h1/span[contains(@itemprop,"name")]/text()').get(default="").strip()
        cur_rating_value = response.xpath('//h1/span[contains(@itemprop,"ratingValue")]/text()').get(default="").strip()
        cur_best_rating = 100
        cur_num_ratings = response.xpath('//h1/span[contains(@itemprop,"ratingCount")]/text()').get(default="").strip()
        cur_logo = response.css("img.logo_med::attr(src)").get(default="").strip()
        cur_logo_url = response.urljoin(cur_logo)
        cur_company_website = response.xpath('//div/a[contains(@itemprop,"sameAs")]/@href').get(default="").strip()
        cur_founding_date = response.xpath('//div[contains(@itemprop,"foundingDate")]/time/@datetime').get(default="").strip()
        cur_founding_country = response.xpath('//div[contains(@itemprop,"foundingLocation")]/text()').get(default="").strip()

        yield {
            'url': cur_url,
            'timestamp_crawl': cur_timestamp,
            'company_name': cur_company_name,
            'rating_value': cur_rating_value,
            'best_rating' : cur_best_rating,
            'num_ratings' : cur_num_ratings,
            'logo_url' : cur_logo_url,
            'company_website' : cur_company_website,
            'founding_date' : cur_founding_date,
            'founding_country' : cur_founding_country
        }
