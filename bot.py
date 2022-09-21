from unicodedata import category
from xml.dom import InvalidAccessErr
import telebot
import json
from update import update

token = ""
admin_pass = ""
admin_chat_id = ""





with open("credentials.json", "r", encoding="UTF-8") as f:
    data = json.load(f)
    print(data)

    try:
        token = data["token"]
    except Exception as e:
        print(e)

    try:
        admin_pass = data["admin_pass"]
    except Exception:
        admin_pass = ""
        admin_chat_id = ""

bot = telebot.TeleBot(token)

users = {}

def password_hander(message):
    if message.text == admin_pass:
        users[message.from_user.id] = "access to service"
        return True
    else:
        return False

def get_data(message):
    if message.text == "Получить изменения":
        changes = ""
        with open("changes.json", "r") as f:
            data = json.load(f)
            data = sorted(data, key=lambda d: d["category"])
            for row in data:
                name = row["name"]
                category = row["category"]
                pricenow = row["price"][-1]["common"]
                priceold = row["price"][0]["common"]
                url = row["url"]
                changes += f"{category}   {name} {priceold} -> {pricenow}  {url}\n"
                
        bot.send_message(message.from_user.id, changes)

actions = {
    "password expected" : password_hander,
    "access to service" : get_data,
}


@bot.message_handler(content_types=["text"])
def registation(message):
    if message.text == "/reg":
        bot.send_message(message.from_user.id, "Введите пароль")
        users[message.from_user.id] = "password expected" 
        print(users)
    else:
        if users.get(message.from_user.id, 0):
            actions[users[message.from_user.id]](message)

bot.polling(none_stop=True, interval=0)