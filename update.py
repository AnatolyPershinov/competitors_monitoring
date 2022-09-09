import json
from typing import NoReturn

from parse_dynam import GoodsFinder


def main():
    old = GoodsFinder()
    try:
        old.get_data_from_json("data.json")
    except FileNotFoundError:
        with open("data.json", "x", encoding="UTF-8"):
            print("file not found. created new file")
    except json.JSONDecodeError:
        print("wrong decode. skip it")

    new = GoodsFinder()
    new.get_data_from_site("https://xn--74-6kcasybqqi.xn--p1ai")

    old, changes = compare(new, old)
    with open("changes.json", "w", encoding="UTF-8") as f:
        print(json.dumps(changes), file=f)

    save_data(old, "data.json")
    

def compare(new: GoodsFinder, old: GoodsFinder):
    new_dict = new.getDict()
    old_dict = old.getDict()
    changes = []

    for k, v in new_dict.items():
        if old_dict.get(k):
            if old_dict[k]["price"][-1]["common"] != v["price"][-1]["common"] or \
            old_dict[k]["price"][-1]["card"] != v["price"][-1]["card"]:
                old_dict[k]["object"].price.append(v["price"])
                changes.append(old_dict[k]["object"].__repr__())
        else:
            old.goods.append(new_dict[k]["object"])
            changes.append(new_dict[k]["object"].__repr__())
    
    return old, changes


def save_data(data: GoodsFinder, filename : str) -> NoReturn: 
    data.save_to_json(filename)

main()
