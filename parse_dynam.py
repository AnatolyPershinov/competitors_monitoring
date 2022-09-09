import requests
import time
import json

from bs4 import BeautifulSoup


class Good():

    def __init__(self, name, category, 
                price, url):

        self.name = name
        self.category = category
        self.price = price
        self.url = url
    

    def __repr__(self):
        return {
            "name" : self.name,
            "category" : self.category,
            "price" : self.price,
            "url" : self.url,
            }
    

    def get_data(self):
        return {
            "category" : self.category,
            "price" : self.price,
            "url" : self.url,
        }


class GoodsFinder():
    def __init__(self):
        self.goods = []


    def get_data_from_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            res = json.loads(f.read())
            for k, v in res.items():
                self.goods.append(Good(
                    name=k, 
                    category = v["category"],
                    price = v["price"],
                    url = v["url"]
                ))


    def get_data_from_site(self, url):
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

                    pricelist = [{
                        "common" : price,
                        "card" : price_card, 
                        "update_time" : int(time.time())
                    }]

                    self.goods.append(
                        Good(name, category, 
                            pricelist, url
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


    def save_to_json(self, filename):
        res = {}
        for good in self.goods:
            res[good.name] = good.get_data()
        
        with open(filename, "w", encoding="utf-8") as f:
            data = json.dumps(res)
            print(data, file=f)


    def getDict(self):
        res = {}
        for good in self.goods:
            res[good.name] = good.get_data()
            res[good.name]["object"] = good

        return res
