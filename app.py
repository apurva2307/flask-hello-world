import telebot
import os
from flask import Flask, request
import requests


app = Flask(__name__)
API_KEY = dict(os.environ)["API_KEY"]
bot = telebot.TeleBot(API_KEY)


def broadcast_messages(list_of_groups, msg):
    for group in list_of_groups:
        to_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={group}&text={msg}&parse_mode=HTML"
        resp = requests.get(to_url)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Thanks for subscribing my service.")


@bot.message_handler(commands=["help"])
def send_welcome(message):
    help_msg = """
    Following are the commands which you can use:
    /help
    ipo <name of company>
    mf <category of mutual fund>
    """
    bot.reply_to(message, help_msg)


def ipo_request(message):
    req = message.text.split()
    if len(req) < 2 or req[0].lower() not in "ipo":
        return False
    else:
        return True


@bot.message_handler(func=ipo_request)
def ipo(message):
    req = message.text.split()[1]
    bot.send_message(message.chat.id, "HI, welcome in world of IPOs..")


@app.route("/")
def hello_world():
    bot.remove_webhook()
    bot.set_webhook(url="https://flask-app-pxeg.onrender.com" + API_KEY)
    return "Hello, World!"


@app.route("/jenu")
def hello_appu():
    broadcast_messages(["641792797"], "I Love you Jenu..")
    return "Hello Apurva"


def parse_message(msg):
    chat_id = msg["message"]["chat"]["id"]
    txt = msg["message"]["text"]
    return chat_id, txt


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    msg = request.get_json()
    chat_id, txt = parse_message(msg)
    print(chat_id)
    print(txt)
    broadcast_messages([chat_id], txt)
    return "!", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
