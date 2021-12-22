import os
from flask import Flask, request
import requests
import json


app = Flask(__name__)
API_KEY = dict(os.environ)["API_KEY"]
API_URL = f"https://api.telegram.org/bot{API_KEY}"
data_url = "https://e-commerce-api-apurva.herokuapp.com/api/v1/telebot"


def broadcast_messages(list_of_groups, msg):
    for group in list_of_groups:
        to_url = f"{API_URL}/sendMessage"
        payload = {"chat_id": group, "text": msg, "parse_mode": "HTML"}
        resp = requests.post(to_url, json=payload)
        return resp


def parse_message(msg):
    chat_id = msg["message"]["chat"]["id"]
    txt = msg["message"]["text"].lower()
    first_name = msg["message"]["chat"]["first_name"]
    username = msg["message"]["chat"]["username"]
    return chat_id, txt, first_name, username


def broadcastToAll(msg):
    usersURL = f"{data_url}/getAllUsers"
    allUsers = requests.get(usersURL).json()
    for user in allUsers["telegramUsers"]:
        broadcast_messages([user["chat_id"]], msg)


def addToDatabase(chat_id, username, first_name):
    registerURL = f"{data_url}/register"
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
    elif command[:5] == "/all " and chat_id == 44114772:
        help_msg = command[5:]
        print(help_msg)
        broadcastToAll(help_msg)
    else:
        broadcast_messages([chat_id], "No such command exists..")


@app.route("/set")
def set_webhook():
    url = dict(os.environ)["WEB_URL"]
    webhook_url = f"{url}/{API_KEY}"
    setWebhook = f"{API_URL}/setWebhook"
    options = {
        "url": webhook_url,
        "allowed_updates": ["message"],
        "drop_pending_updates": True,
    }
    requests.post(setWebhook, json=options)
    return "Webhook has been set."


@app.route("/clear")
def delete_webhook():
    deleteWebhook = f"{API_URL}/deleteWebhook"
    options = {"drop_pending_updates": True}
    requests.post(deleteWebhook, json=options)
    return "Webhook has been removed."


@app.route("/get")
def get_webhook_info():
    getWebhookInfo = f"{API_URL}/getWebhookInfo"
    resp = requests.get(getWebhookInfo)
    return json.dumps(resp.json()["result"])


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/jenu")
def hello_appu():
    broadcast_messages(["641792797"], "I Love you Jenu..")
    return "Hello Apurva"


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    msg = request.get_json()
    chat_id, txt, first_name, username = parse_message(msg)
    if txt == "/start" or txt == "/subscribe":
        response = addToDatabase(chat_id, username, first_name).json()
        broadcast_messages(["44114772"], json.dumps(response))
        broadcast_messages(["44114772"], chat_id)
        broadcast_messages(["44114772"], username)
        broadcast_messages([chat_id], "Thanks for subscribing my service.")
    elif is_command(txt):
        execute_command(txt, chat_id)
    else:
        broadcast_messages([chat_id], txt)
    return "!", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
