import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import json

class IGDBGamesSpider(scrapy.Spider):
    name = "igdb_games"
    max_count = -1

    start_urls = ["https://www.igdb.com/categories?page=1"]

    def __init__(self):
        self.cur_count = 0

    def parse(self, response):
        # Category page links: response.xpath('//a[contains(@href,"/categories/")]/@href').getall()
        # Next page link: response.css("li.next a::attr(href)").get()

        # Follow the category page links:
        for href in response.xpath('//a[contains(@href,"/categories/")]/@href'):
            yield response.follow(href, self.parse_category_page, meta={'cur_page_num': 2})

        # Follow next page links:
        for href in response.css("li.next a::attr(href)"):
            yield response.follow(href, self.parse)


    def parse_category_page(self, response):
        cur_page_num = response.meta.get('cur_page_num')
        # Game page links: response.css("div.media-body a::attr(href)").getall()
        # Next page (AJAX request) link: https://www.igdb.com/categories/sci-fi/?rating=desc&page=%s

        # Follow the game page links:
        is_games_available = False
        for href in response.css("div.media-body a::attr(href)"):
            is_games_available = True
            self.cur_count = self.cur_count + 1
            if self.max_count != -1 and self.cur_count >= self.max_count:
                return
            yield response.follow(href, self.parse_game_page)

        # Follow next page link:
        if is_games_available:
            cur_url = response.url.split("?")[0]
            next_page_url = (cur_url + "?rating=desc&page={}").format(cur_page_num)
            yield response.follow(next_page_url, self.parse_category_page, meta={'cur_page_num': cur_page_num+1})
        else:
            return


    def parse_game_page(self, response):
        # Name: response.css("h1.banner-title::text").get()
        # Release date: response.xpath('//span[contains(@itemprop,"datePublished")]/time/@datetime').get()
        # Game website links: response.xpath('//a[contains(@class,"gamepage-website-link")]/@href').getall()
        # Game description: response.css("div.gamepage-tabs div::text").getall()

        # Platform names: response.xpath('//p/a[contains(@href,"/platforms/")]/text()').getall()
        # Platform urls: response.xpath('//p/a[contains(@href,"/platforms/")]/@href').getall()

        # Developer name: response.xpath('//div[contains(@itemprop,"author")]/span/a/text()').getall()
        # Developer url: response.xpath('//div[contains(@itemprop,"author")]/span/a/@href').getall()

        # Publisher name: response.xpath('//span[contains(@itemprop,"publisher")]/span/a/text()').getall()
        # Publisher url: response.xpath('//span[contains(@itemprop,"publisher")]/span/a/@href').getall()

        # Game modes: response.xpath('//a[contains(@itemprop,"playMode")]/text()').getall()
        # Genre: response.xpath('//a[contains(@itemprop,"genre")]/text()').getall()
        # Themes: response.xpath('//a[contains(@href,"/themes/")]/text()').getall()

        # Keywords:
        # json_obj = response.xpath('//div[contains(@data-react-class,"ReadMore")]/@data-react-props').get()
        # parsed_dict = json.loads(json_obj)
        # urls = parsed_dict['html'].split(",")
        # cur_href = urls[0].split("\"")[1]

        # Game rating: response.css("svg text::text").getall()
        # Game num rating counts: response.xpath('//div[contains(@class,"gauge-single-info")]/text()').getall()
        # Content rating: response.xpath('//span[contains(@itemprop,"contentRating")]/text()').getall()

        # Extract the game description using Beautiful soup:
        try:
            parsed_soup = BeautifulSoup(response.text, "html.parser")
            json_text = parsed_soup.find('div', {'data-react-class': "GamePageHeader"})['data-react-props']
            game_summary = json.loads(json_text)["summary"]
        except:
            game_summary = ""

        # Extract all the attributes of the game:
        cur_url = str(response.url)
        cur_timestamp = str(datetime.utcnow())
        game_name = response.css("h1.banner-title::text").get(default="").strip()
        game_website_links = response.xpath('//a[contains(@class,"gamepage-website-link")]/@href').getall()
        release_date = response.xpath('//span[contains(@itemprop,"datePublished")]/time/@datetime').get(default="").strip()


        platform_names = response.xpath('//p/a[contains(@href,"/platforms/")]/text()').getall()
        platform_urls_rel = response.xpath('//p/a[contains(@href,"/platforms/")]/@href').getall()
        platform_urls = []
        for relative_url in platform_urls_rel:
            url = response.urljoin(relative_url)
            platform_urls.append(url)

        developer_names = response.xpath('//div[contains(@itemprop,"author")]/span/a/text()').getall()
        developer_urls_rel = response.xpath('//div[contains(@itemprop,"author")]/span/a/@href').getall()
        developer_urls = []
        for relative_url in developer_urls_rel:
            url = response.urljoin(relative_url)
            developer_urls.append(url)

        publisher_names = response.xpath('//span[contains(@itemprop,"publisher")]/span/a/text()').getall()
        publisher_urls_rel = response.xpath('//span[contains(@itemprop,"publisher")]/span/a/@href').getall()
        publisher_urls = []
        for relative_url in publisher_urls_rel:
            url = response.urljoin(relative_url)
            publisher_urls.append(url)

        game_modes = response.xpath('//a[contains(@itemprop,"playMode")]/text()').getall()
        genres = response.xpath('//a[contains(@itemprop,"genre")]/text()').getall()
        themes = response.xpath('//a[contains(@href,"/themes/")]/text()').getall()

        ratings = response.css("svg text::text").getall()
        if len(ratings) != 0:
            game_rating = ratings[0]
        else:
            game_rating = -1

        rating_counts = response.xpath('//div[contains(@class,"gauge-single-info")]/text()').getall()
        if len(rating_counts) != 0:
            num_rating_counts = rating_counts[-1]
        else:
            num_rating_counts = -1

        content_ratings = response.xpath('//span[contains(@itemprop,"contentRating")]/text()').getall()

        yield {
            'url': cur_url,
            'timestamp_crawl': cur_timestamp,
            'game_name': game_name,
            'game_summary': game_summary,
            'game_website_links': game_website_links,
            'release_date': release_date,
            'platform_names': platform_names,
            'platform_urls': platform_urls,
            'developer_name': developer_names,
            'developer_url': developer_urls,
            'publisher_name': publisher_names,
            'publisher_url': publisher_urls,
            'game_modes': game_modes,
            'genre': genres,
            'themes': themes,
            'game_rating': game_rating,
            'num_rating_counts': num_rating_counts,
            'content_rating': content_ratings
        }
