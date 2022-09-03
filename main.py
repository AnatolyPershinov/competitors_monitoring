import json
from typing import NoReturn

from parse_dynam import GoodsFinder


def main():
    read_data("data.json")
    
    rowdata = GoodsFinder("https://xn--74-6kcasybqqi.xn--p1ai")
    save_data(rowdata, "data.json")


def read_data(filename : str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        res = json.loads(f.read())
    return res


def compare(new : GoodsFinder, old : dict) -> dict:
    for good in new.goods:
        old_good = old.get(good.name) 
        if old_good != None:
            if 


def save_data(data: GoodsFinder, filename : str) -> NoReturn: 
    with open(filename, "w", encoding="utf-8") as f:
        data = json.dumps(data.getDict())
        print(data, file=f)

main()
