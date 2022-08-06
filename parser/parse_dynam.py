import requests

from bs4 import BeautifulSoup
from datetime import datetime


class Good():
    name = ""
    category = ""
    price = 0
    card_price = 0
    update_time = 0
    url = ""

    def __init__(self, name, category, 
                price, card_price, url):
        self.name = name
        self.category = category
        self.price = price
        self.card_price = card_price
        self.url = url
        self.update_time = datetime.now()

    def __repr__(self):
        return f"{self.category} {self.name} {self.price} {self.card_price} {self.url} {self.update_time}"


class GoodsFinder():
    Goods = []

    def __init__(self, url):
        self.url = url
        self.session = requests.session()
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        stage1 = soup.findAll("li", class_="menu_item")
        links = []

        for row in stage1:
            links.append(row.findAll('a')[0].get('href'))
        self.parse_catalog(links)

    def parse_goods(self, link, page):
        result = []
        for i in range(1, page+1):
            param = dict(PAGEN_1=i)
            res = self.session.get(self.url+link, params=param)
            soup = BeautifulSoup(res.text, "html.parser")
            goods = soup.findAll("div", class_="catalog_item item_wrap")
            category = soup.select("h1")[0].text
            for good in goods:
                
                try:
                    name = good.findAll("div", class_="item-title")[0].findAll("span")[0].text
                    price = good.findAll("div", class_="price")[0]["data-value"]
                    price_card = good.findAll("div", class_="price d74")[0]["data-value"]
                    url = good.select("a")[0]["href"]
                    
                    if price.find("\\xa0"):
                        price = price.replace("\\xa0", "")
                    
                    if price_card.find("\\xa0"):
                        price_card = price_card.replace("\\xa0", "")

                    self.Goods.append(
                        Good(name, category, 
                            price, price_card, url
                    ))

                except Exception as e:
                    print(f"error with {self.url+link}: \n {e}")
                

        
    def parse_catalog(self, links):
        result = {}

        for link in links:
            res = self.session.get(self.url+link)
            soup = BeautifulSoup(res.text, "html.parser")
            name = soup.findAll('title')[0].text[:-12]
            try: 
                max_page = int(soup.findAll("div", class_="nums")[0].findAll("a")[-1].text)
            except Exception:
                max_page = 1
                
            self.parse_goods(link, max_page)
