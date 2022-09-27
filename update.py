import json

from parse_dynam import Good, GoodsFinder


def update():
    old = GoodsFinder()
    try:
        old.get_data_from_json("data.json")
    except FileNotFoundError:
        with open("data.json", "x", encoding="UTF-8"):
            print("file not found. created new file")
    except json.JSONDecodeError:
        print("wrong decode. skip it")

    new = GoodsFinder()
    new.get_data_from_site()

    
    old, changes = compare(new, old)
    
    save_data(changes, "changes.json")
    save_data(old, "data.json")
    
    return changes
    

def compare(new: GoodsFinder, old: GoodsFinder):
    new_dict = new.getDict()
    old_dict = old.getDict()
    changes = GoodsFinder()

    for k, v in new_dict.items():
        if old_dict.get(k):
            if old_dict[k]["price"][-1]["common"] != v["price"][-1]["common"] or \
            old_dict[k]["price"][-1]["card"] != v["price"][-1]["card"]:
                old_dict[k]["object"].price.append(v["price"])
                changes.goods.append(old_dict[k]["object"])
        else:
            old.goods.append(new_dict[k]["object"])
            changes.goods.append(new_dict[k]["object"])
    
    return old, changes


def save_data(data: GoodsFinder, filename : str): 
    data.save_to_json(filename)
