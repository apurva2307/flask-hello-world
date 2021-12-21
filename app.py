import telebot
import os
from flask import Flask, request
import requests

app = Flask(__name__)
API_KEY = dict(os.environ)["API_KEY"]
bot = telebot.TeleBot(API_KEY)


def broadcast_messages(list_of_groups, msg):
    for group in list_of_groups:
        to_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"
        payload = {"chat_id": group, "text": msg, "parse_mode": "HTML"}
        resp = requests.post(to_url, json=payload)


def parse_message(msg):
    print("type of msg:>", type(msg))
    chat_id = msg["message"]["chat"]["id"]
    txt = msg["message"]["text"]
    first_name = msg["message"]["chat"]["first_name"]
    username = msg["message"]["chat"]["username"]

    return chat_id, txt, first_name, username


url = "https://e-commerce-api-apurva.herokuapp.com/api/v1/telebot"


def broadcastToAll(msg):
    usersURL = f"{url}/getAllUsers"
    allUsers = requests.get(usersURL).json()
    allUsersList = []
    for user in allUsers["telegramUsers"]:
        allUsersList.append(user["chat_id"])
    broadcast_messages(allUsersList, msg)


def addToDatabase(chat_id, username, first_name):
    registerURL = f"{url}/register"

    payload = {"chat_id": chat_id, "username": username, "first_name": first_name}
    resp = requests.post(registerURL, json=payload)
    return resp


def is_command(txt):
    return txt[0] == "/"


def execute_command(command, chat_id):
    if command == "/ipo":
        broadcast_messages([chat_id], "HI, welcome in world of IPOs..")
    elif command == "/help":
        help_msg = "<pre>Following are the options:</pre>"
        print(help_msg)
        broadcast_messages([chat_id], help_msg)
    else:
        broadcast_messages([chat_id], "No such command exists..")


@app.route("/")
def hello_world():
    bot.remove_webhook()
    bot.set_webhook(url="https://flask-app-pxeg.onrender.com/" + API_KEY)
    # bot.set_webhook(url="https://4f8f-106-214-77-65.ngrok.io/" + API_KEY)
    return "Hello, World!"


@app.route("/jenu")
def hello_appu():
    broadcast_messages(["641792797"], "I Love you Jenu..")
    return "Hello Apurva"


@app.route("/all")
def broadcasttousers():
    broadcastToAll("Hi everone..")
    return "Hi to all"


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    msg = request.get_json()
    chat_id, txt, first_name, username = parse_message(msg)
    print(chat_id, first_name, username, txt)
    if txt == "/start":
        print(">>start<<")
        response = addToDatabase(chat_id, username, first_name).json()
        print(response)
        broadcast_messages([chat_id], "Thanks for subscribing my service.")
    elif is_command(txt):
        execute_command(txt, chat_id)
    else:
        broadcast_messages([chat_id], txt)
    return "!", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
