import os
from flask import Flask, request
import requests
import json
from helpers import sendFile, broadcast_messages, parse_request, broadcast_items
from database import broadcastToAll, addToDatabase
from decouple import config


app = Flask(__name__)
API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"


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
        broadcast_items([chat_id], command[8:], "Photo")
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
    chat_id, txt, first_name, username = parse_request(req)
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
        sendFile(chat_id, "txt", "files/requirements.txt", "requirements.txt")
        broadcast_items([chat_id], txt, "Document")
    return "!", 200


if config("ENVIRON") == "DEV":
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)
