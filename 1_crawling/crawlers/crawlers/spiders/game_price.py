import scrapy
import json
import re
from bs4 import BeautifulSoup
from scrapy import Request
import requests
from scrapy.exceptions import CloseSpider
import time
from datetime import datetime
from urllib.parse import urlparse




def info_extractor(prod):
    """
    :param prod: soup object for game
    :return: surface level info - title of game, new price, url, discount, old price, logo of the game
    """
    title_soup = prod.find('h3',class_ = "Card__title")
    title = title_soup.find('a')
    if title is not None:
        title = title.get_text()
    url_page = title_soup.find('a')['href']
    price = prod.find('span',class_ = 'Card__price-cost price')
    if price is not None:
        price = price.get_text()
    old_price = prod.find('span',class_ = 'old-price')
    if old_price != None:
        old_price = old_price.get_text()
    discount = prod.find('span',class_ = 'percent')
    if discount != None:
        discount = discount.get_text()

    img_url = prod.find('img',class_ = 'lazy-image__img')['data-src']
    return title,price,old_price,discount,url_page,img_url

def level_one_parser(soup_next):
    """
    :param soup_next: soup object for depth 1 page of the game
    :return: seller name, seller rating, seller feedback message, price of the game sold by the seller, old price of the game,
    discount provided by the seller, description of the game, minimum requirements of the game, recommended requirements
    """
    desc = []
    zipped_list = []
    min_r = {}
    recom_r = {}
    best_seller = soup_next.find('div',class_ = 'seller-info')
    best_seller_price_info = soup_next.find('div',class_ = 'product-page-v2-price payments__price product-page-v2-price--large')
    seller_name = best_seller.find('span',class_ = 'seller-info__user')
    unstruct_soup = soup_next.find('div',class_='product-section__content__content--default-section')
    require_soup = soup_next.find('div',{'data-name' : 'Windows' } )
    if seller_name != None:
        seller_name = seller_name.get_text()
    seller_rating = best_seller.find('span',class_ = 'seller-info__percent')
    if seller_rating != None:
        seller_rating = seller_rating.get_text()
    seller_feedback_msg = best_seller.find('span',class_ = 'seller-info__feedback-message')
    if seller_feedback_msg is not None:
        seller_feedback_msg = seller_feedback_msg.get_text()
    seller_price = best_seller_price_info.find('div',class_ = 'product-page-v2-price__price')
    if seller_price is not None:
        seller_price = seller_price.get_text()
    seller_old_price = best_seller_price_info.find('span',class_ = 'product-page-v2-price__old-price')
    if seller_old_price is not None:
        seller_old_price = seller_old_price.get_text()
    seller_discount = best_seller_price_info.find('span',class_ = 'product-page-v2-price__discount')
    if seller_discount is not None:
        seller_discount = seller_discount.get_text()
    if unstruct_soup is not None:
        para = unstruct_soup.find_all('p')
        if para is not None:
            for p in para:
                desc.append((p.get_text()))
    if require_soup is not None:
        print('y1')
        min_recom_soup = require_soup.find_all('ul')
        if min_recom_soup is not None:
            print('y2')
            print(min_recom_soup)
            for i,ul in enumerate(min_recom_soup):
                print('y3')
                zipped_list = list(zip(ul.find_all('span',class_ = 'attributes-list__name'),ul.find_all('span',class_ = 'attributes-list__value')))
                if i == 0:
                    for val in zipped_list:
                        key = val[0].get_text()
                        value = val[1].get_text()
                        min_r[key] = value
                if i == 1:
                    for val in zipped_list:
                        key = val[0].get_text()
                        value = val[1].get_text()
                        recom_r[key] = value

    return seller_name,seller_rating,seller_feedback_msg,seller_price,seller_old_price,seller_discount,desc,min_r,recom_r




class imdb_spider(scrapy.Spider):
    name = 'game_cost_scraper'
    urls = ['https://www.g2a.com/en-us/category/gaming-c1']
    allowed_domains = ['g2a.com']
    for it in range(2,6, 1):
        urls.append('https://www.g2a.com/en-us/category/gaming-c1?page={}'.format(it))

    custom_settings = {
        #'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        #'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # 'DUPEFILTER_CLASS': 'custom_filter.SeenURLFilter',
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
        'CONCURRENT_REQUESTS': 50,
        'RETRY_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 15,
        'REDIRECT_ENABLED': False,
        'DEPTH_LIMIT': 1
    }
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url,callback = self.game_parser)

    def game_parser(self, response):
        '''
        :param response: is the crawled page by scrapy spider
        :yields: jsonline for each game with various attributes like game name, seller information, requirements
        '''

        if response.status == 200:
            if response.meta['depth'] == 0:
                soup = BeautifulSoup(response.text,'html.parser')
                products = soup.find_all('li',class_='products-grid__item')
                for prod in products:

                    d = {'title': '', 'price': '', 'url': '', 'seller_name': '', 'seller_rating': '',
                         'seller_feedback_msg':'','seller_price':'','seller_old_price':'','seller_discount':'',
                         'old_price': '' , 'discount': '','min_requirements':'','recommended_requirements':'','img_url':'','desc' : ''}
                    title,price,old_price,discount,url_page,img_url = info_extractor(prod)
                    url_follow = response.urljoin(url_page)
                    d['title'] = title
                    d['price'] = price
                    d['old_price'] = old_price
                    d['discount'] = discount
                    d['url'] = url_follow
                    d['img_url'] = img_url
                    yield response.follow(url_follow,self.game_parser,meta = d)

            if response.meta['depth'] == 1:
                #print('yes')
                #drum = {'seller_name':'' , "seller_rating":''}
                soup_next = BeautifulSoup(response.text,'html.parser')
                seller_name,seller_rating,seller_feedback_msg,seller_price,seller_old_price,seller_discount,desc,min_r,recom_r = level_one_parser(soup_next)
                response.meta['seller_name'] = seller_name
                response.meta['seller_rating'] = seller_rating
                response.meta['seller_feedback_msg'] = seller_feedback_msg
                response.meta['seller_price'] = seller_price
                response.meta['seller_old_price'] = seller_old_price
                response.meta['seller_discount'] = seller_discount
                response.meta['desc'] = desc
                response.meta['min_requirements'] = min_r
                response.meta['recommended_requirements'] = recom_r
                yield {"title": response.meta['title'], "price": response.meta['price'], "url": response.meta['url'],
                       "seller_name":response.meta['seller_name'],"seller_rating":response.meta['seller_rating'],
                       'seller_feedback_msg':response.meta['seller_feedback_msg'],'seller_price':response.meta['seller_price'],
                       'seller_old_price':response.meta['seller_old_price'],'seller_discount':response.meta['seller_discount']
                       ,"old_price":response.meta['old_price'],"discount":response.meta['discount'],
                       "min_requirements":response.meta['min_requirements'],"recommended_requirements":response.meta['recommended_requirements'],
                       "img_url":response.meta['img_url'],'desc':response.meta['desc']}

