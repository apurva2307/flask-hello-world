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


def parse_message(msg):
    chat_id = msg["message"]["chat"]["id"]
    txt = msg["message"]["text"]
    return chat_id, txt

def is_command(txt):
    return txt[0] == "/"


def execute_command(command, chat_id):
    if command == "/ipo":
        broadcast_messages([chat_id], "HI, welcome in world of IPOs..")
    elif command == "/start":
        broadcast_messages([chat_id], "Thanks for subscribing my service.")
    elif command == "/help":
        help_msg = """
        Following are the commands which you can use:
        /help
        ipo <name of company>
        mf <category of mutual fund>
        """
        broadcast_messages([chat_id], help_msg)
    else:
        broadcast_messages([chat_id], "No such command exists..")


@app.route("/")
def hello_world():
    bot.remove_webhook()
    bot.set_webhook(url="https://flask-app-pxeg.onrender.com/" + API_KEY)
    return "Hello, World!"


@app.route("/jenu")
def hello_appu():
    broadcast_messages(["641792797"], "I Love you Jenu..")
    return "Hello Apurva"


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    msg = request.get_json()
    chat_id, txt = parse_message(msg)
    if is_command(txt):
        execute_command(txt, chat_id)
    else:
        broadcast_messages([chat_id], txt)
    return "!", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
