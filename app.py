import os
from flask import Flask, request
import requests
import json
import keys

app = Flask(__name__)
API_KEY = dict(os.environ)["API_KEY"]
API_URL = f"https://api.telegram.org/bot{API_KEY}"
data_url = "https://e-commerce-api-apurva.herokuapp.com/api/v1/telebot"
content = ""


def broadcast_messages(list_of_groups, msg):
    for group in list_of_groups:
        to_url = f"{API_URL}/sendMessage"
        payload = {"chat_id": group, "text": msg, "parse_mode": "HTML"}
        resp = requests.post(to_url, json=payload)
        return resp


def broadcast_items(list_of_groups, item, type):
    for chat_id in list_of_groups:
        to_url = f"{API_URL}/send{type}"
        if type == "Sticker":
            payload = {"chat_id": chat_id, "sticker": item}
        if type == "Photo":
            payload = {"chat_id": chat_id, "photo": item}
        if type == "Document":
            payload = {"chat_id": chat_id, "document": item}
        resp = requests.post(to_url, json=payload)
        return json.dumps(resp.json())


def parse_request(req):
    chat_id = req["message"]["chat"]["id"]
    if "text" in req["message"].keys():
        txt = req["message"]["text"].lower()
    elif "sticker" in req["message"].keys():
        txt = req["message"]["sticker"]["file_id"]
    elif "document" in req["message"].keys():
        txt = req["message"]["document"]["file_id"]
    elif "photo" in req["message"].keys():
        txt = req["message"]["photo"][0]["file_id"]
    first_name = req["message"]["chat"]["first_name"]
    username = req["message"]["chat"]["username"]
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
        broadcast_messages([chat_id], help_msg)
    elif (
        command[:5].lower() == "/all "
        and chat_id == 44114772
        and command[5:8].lower() == "img"
    ):
        content = "img"
        print(content)
    elif command[:5] == "/all " and chat_id == 44114772:
        msg = command[5:]
        broadcastToAll(msg)
    else:
        broadcast_messages([chat_id], "No such command exists..")


@app.route("/set")
def set_webhook():
    url = dict(os.environ)["WEB_URL"]
    webhook_url = f"{url}/{API_KEY}"
    setWebhook = f"{API_URL}/setWebhook"
    options = {
        "url": webhook_url,
        "allowed_updates": ["message", "channel_post"],
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
    req = request.get_json()
    print("req>>", req)
    print("content>", content)
    chat_id, txt, first_name, username = parse_request(req)
    if content == "":
        if "text" in req["message"].keys():
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
        if "sticker" in req["message"].keys():
            broadcast_items([chat_id], txt, "Sticker")
        if "photo" in req["message"].keys():
            broadcast_items([chat_id], txt, "Photo")
        if "document" in req["message"].keys():
            broadcast_items([chat_id], txt, "Document")
    elif content == "img":
        broadcast_items([chat_id], txt, "Photo")
    return "!", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
