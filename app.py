from flask import Flask, request
import requests, pickle, os, json
from helpers import (
    broadcast_to_admin,
    broadcastToAll,
    sendFile,
    broadcast_msg,
    parse_request,
    broadcast_items,
    execute_command,
    is_command,
)
from database import get_all_users, addToDatabase
from decouple import config


app = Flask(__name__)
API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"


@app.route("/set")
def set_webhook():
    url = config("WEB_URL")
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
    return "Hello, Invest Advice Bot"


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    req = request.get_json()
    print("req>>", req)
    chat_id, txt, first_name, username = parse_request(req)
    if os.path.isfile("img.pkl"):
        users = get_all_users()
        for user in users:
            broadcast_items(user["chatId"], txt, "Photo")
        os.remove("img.pkl")
    if os.path.isfile("file.pkl"):
        users = get_all_users()
        for user in users:
            broadcast_items(user["chatId"], txt, "Document")
        os.remove("file.pkl")
    if "text" in req["message"].keys():
        if txt == "/start" or txt == "/subscribe":
            response = addToDatabase(chat_id, username, first_name)
            if "already exists" in response["msg"]:
                broadcast_msg(chat_id, "You have already subscribed to this bot.")
            else:
                broadcast_msg(chat_id, "Thanks for subscribing this bot.")
                broadcast_msg(44114772, json.dumps(response))
                broadcast_msg(44114772, chat_id)
                broadcast_msg(44114772, f"@{username}")
        elif is_command(txt):
            execute_command(txt, chat_id)
        else:
            if chat_id == 44114772:
                broadcastToAll(txt)
            else:
                broadcast_to_admin(f"{txt}\nsent by {first_name}\n@{username}")
    # if "sticker" in req["message"].keys():
    #     broadcast_items(chat_id, txt, "Sticker")
    # if "photo" in req["message"].keys():
    #     broadcast_items(chat_id, txt, "Photo")
    # if "document" in req["message"].keys():
    #     sendFile(chat_id, "txt", "requirements.txt", "requirements.txt")
    #     broadcast_items(chat_id, txt, "Document")
    return "!", 200


if config("ENVIRON") == "DEV":
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)
