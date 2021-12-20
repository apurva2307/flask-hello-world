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
        print(resp.text)


@app.route("/")
def hello_world():
    bot.remove_webhook()
    bot.set_webhook(url="https://flask-app-pxeg.onrender.com/" + API_KEY)
    broadcast_messages(["641792797"], "HI from bot")
    return "Hello, World!"


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        return "!", 200


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


bot.infinity_polling()
