import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

class TechPowerUPGPUSpecs(scrapy.Spider):
    name = "techpowerup_gpu_specs"
    max_count = -1

    start_urls = ["https://www.techpowerup.com/gpu-specs/"]

    def __init__(self):
        self.cur_count=0

    def parse(self, response):
        # Get generation options:
        soup = BeautifulSoup(response.text, "html.parser")
        gens = soup.find(id="generation")
        var_options = gens.find_all("option")
        gens_vals = []
        for cur_option in var_options:
            cur_val = cur_option.get("value")
            if len(cur_val) != 0:
                gens_vals.append(cur_val)

        # Follow the generation links:
        base_url = "https://www.techpowerup.com/gpu-specs/?generation={}&sort=name"
        for cur_val in gens_vals:
            cur_url = base_url.format(quote(cur_val))
            self.cur_count = self.cur_count + 1
            if self.max_count != -1 and self.cur_count >= self.max_count:
                return
            yield response.follow(cur_url, self.parse_generation_page)


    def parse_generation_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        proc_table = soup.find("table", {"class": "processors"})

        col_header = proc_table.find("thead", {"class": "colheader"})
        cols_elements = col_header.find_all("th")
        cols_list = []
        for element in cols_elements:
            cols_list.append(element.contents[0])

        cur_row = col_header.find_next("tr").find_next("tr")
        while cur_row is not None:
            cur_dict = {}
            col_index = 0

            for cur_td in cur_row.find_all("td"):
                cur_col = cols_list[col_index]

                has_a = cur_td.find("a")
                if has_a is not None:
                    cur_val = has_a.contents[0]
                    if cur_col == "Product Name":
                        cur_dict["product_name_url"] = response.urljoin(str(has_a.get("href")))
                    elif cur_col == "GPU Chip":
                        cur_dict["gpu_chip_url"] = response.urljoin(str(has_a.get("href")))
                else:
                    cur_val = cur_td.contents[0]

                cur_dict[cur_col] = cur_val
                col_index = col_index + 1

            yield cur_dict
            cur_row = cur_row.find_next("tr")