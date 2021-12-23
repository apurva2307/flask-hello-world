import requests
import os
import json
from decouple import config
from helpers import broadcast_messages

# data_url = dict(os.environ)["DATA_URL"]
data_url = config("DATA_URL")


def addToDatabase(chat_id, username, first_name):
    registerURL = f"{data_url}/register"
    payload = {"chat_id": chat_id, "username": username, "first_name": first_name}
    resp = requests.post(registerURL, json=payload)
    return resp


def broadcastToAll(msg):
    usersURL = f"{data_url}/getAllUsers"
    allUsers = requests.get(usersURL).json()
    for user in allUsers["telegramUsers"]:
        broadcast_messages([user["chat_id"]], msg)
