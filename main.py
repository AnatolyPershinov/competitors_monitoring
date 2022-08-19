import json
import os.path
from datetime import datetime, date

from parse_dynam import GoodsFinder

def json_serial(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def main():
    rowdata = GoodsFinder("https://xn--74-6kcasybqqi.xn--p1ai")
    with open("data.json", "w", encoding="utf-8") as f:
        print(data)
        data = json.dumps(rowdata.getDict())
        print(data, file=f)

main()
