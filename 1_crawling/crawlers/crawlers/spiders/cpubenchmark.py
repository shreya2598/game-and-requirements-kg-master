import scrapy
from bs4 import BeautifulSoup

class CPUBenchmark(scrapy.Spider):
    name = "cpubenchmark_cpus"
    max_count = -1

    start_urls = ["https://www.cpubenchmark.net/CPU_mega_page.html"]

    def parse(self, response):
        # Get CPU Benchmarks:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody")

        for cur_row in table.find_all("tr"):
            cur_id = cur_row.get("id")
            if cur_id is None:
                continue
            cur_dict = {}
            name_ele = cur_row.find_next("td")
            cur_dict["cpu_name"] = name_ele.get_text()

            price_ele = name_ele.find_next("td")
            cur_price = price_ele.get_text()

            '''try:
                cur_price = price_ele.contents[0].contents[0]
            except:
                cur_price = price_ele.contents[0]'''
            cur_dict["price"] = cur_price

            cpu_mark = price_ele.find_next("td")
            cur_dict["cpu_mark"] = cpu_mark.get_text()

            cpu_value = cpu_mark.find_next('td')
            cur_dict['cpu_value'] = cpu_value.get_text()

            thread_mark = cpu_value.find_next('td')
            cur_dict['thread_mark'] = thread_mark.get_text()

            thread_value = thread_mark.find_next('td')
            cur_dict['thread_value'] = thread_value.get_text()

            tdp_w = thread_value.find_next('td')
            cur_dict['tdp_w'] = tdp_w.get_text()

            power_perf = tdp_w.find_next('td')
            cur_dict['power_perf'] = power_perf.get_text()

            test_date = power_perf.find_next('td')
            cur_dict['test_date'] = test_date.get_text()

            socket = test_date.find_next('td')
            cur_dict['socket'] = socket.get_text()

            category = socket.find_next('td')
            cur_dict['category'] = category.get_text()

            yield cur_dict

