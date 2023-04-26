import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import re

class IGDBPlatformsSpider(scrapy.Spider):
    name = "igdb_platforms"
    max_count = -1

    start_urls = ["https://www.igdb.com/platforms"]

    def __init__(self):
        self.cur_count=0

    def parse(self, response):
        # Platform page links: response.xpath('//a[contains(@href,"/platforms/")]/@href').getall()

        # Follow the platform page links:
        for href in response.xpath('//a[contains(@href,"/platforms/")]/@href'):
            self.cur_count = self.cur_count + 1
            if self.max_count!=-1 and self.cur_count >= self.max_count:
                return
            yield response.follow(href, self.parse_platform_page)

    def parse_platform_page(self, response):
        # Name: response.css("h1::text").get()
        # Platform website: response.css("div.btn-group a::attr(href)").get()

        result_dict = {}
        result_dict["url"] = str(response.url)
        result_dict["timestamp_crawl"] = str(datetime.utcnow())
        result_dict["platform_name"] = response.css("h1::text").get(default="").strip()
        result_dict["platform_website"] = response.css("div.btn-group a::attr(href)").get(default="").strip()

        soup = BeautifulSoup(response.text, "html.parser")

        # Manufacturer and developer
        manf = soup.find("h6", text=re.compile(r"Manufacturer"))
        if manf is not None:
            result_dict["manufacturer"] = manf.find_next().get_text()

        dev = soup.find("h6", text=re.compile(r"Developer"))
        if dev is not None:
            result_dict["developer"] = dev.find_next().get_text()

        # Platform Info:
        info = soup.find(id="platform-info")
        if info is not None:
            h6s = info.find_all("h6")
            ahrefs = info.find_all("a")

            try:
                key = h6s[0].get_text()
                val = ahrefs[0].get_text()
                result_dict[key] = val

                key = h6s[1].get_text()
                val = ahrefs[1].get_text()
                result_dict[key] = val

                key = h6s[2].get_text()
                val = ahrefs[2].get_text()
                result_dict[key] = val
            except:
                pass

        # Platform Hardware Info: (Table)
        hinfo = soup.find(id="platform-hardware")
        if hinfo is not None:
            trs = hinfo.find_all("tr")
            for cur_tr in trs:
                th = cur_tr.find_all("th")
                td = cur_tr.find_all("td")

                try:
                    key = th[0].get_text()
                    val = td[0].get_text()
                    result_dict[key] = val

                    key = th[1].get_text()
                    val = td[1].get_text()
                    result_dict[key] = val
                except:
                    pass

        yield result_dict

