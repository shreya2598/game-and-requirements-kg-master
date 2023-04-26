import scrapy
from bs4 import BeautifulSoup

class VideocardBenchmarkGPU(scrapy.Spider):
    name = "videocardbenchmark_gpus"
    max_count = -1

    start_urls = ["https://www.videocardbenchmark.net/GPU_mega_page.html"]

    def parse(self, response):
        # Get GPU Benchmarks:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody")

        for cur_row in table.find_all("tr"):
            cur_id = cur_row.get("id")
            if cur_id is None:
                continue

            cur_dict = {}
            name_ele = cur_row.find_next("td")
            cur_dict["videocard_name"] = name_ele.contents[1].contents[0]

            price_ele = name_ele.find_next("td")
            try:
                cur_price = price_ele.contents[0].contents[0]
            except:
                cur_price = price_ele.contents[0]
            cur_dict["price"] = cur_price

            g3d_ele = price_ele.find_next("td")
            cur_dict["g3d_mark"] = g3d_ele.contents[0]

            videocard_value_ele = g3d_ele.find_next("td")
            try:
                cur_value  = videocard_value_ele.contents[0].contents[0]
            except:
                cur_value = videocard_value_ele.contents[0]
            cur_dict["videocard_value"] = cur_value

            g2d_ele = videocard_value_ele.find_next("td")
            cur_dict["g2d_mark"] = g2d_ele.contents[0]

            tdp_ele = g2d_ele.find_next("td")
            cur_dict["tdp_watt"] = tdp_ele.contents[0]

            power_perf_ele = tdp_ele.find_next("td")
            cur_dict["power_performance"] = power_perf_ele.contents[0]

            test_date_ele = power_perf_ele.find_next("td")
            cur_dict["test_date"] = test_date_ele.contents[0]

            category_ele = test_date_ele.find_next("td")
            cur_dict["category"] = category_ele.contents[0]

            yield cur_dict
