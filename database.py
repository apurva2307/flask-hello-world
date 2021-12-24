import requests, json
from decouple import config

data_url = config("DATA_URL")


def addToDatabase(chat_id, username, first_name):
    registerURL = f"{data_url}/register"
    payload = {
        "chatId": chat_id,
        "username": username,
        "first_name": first_name,
    }
    resp = requests.post(registerURL, json=payload)
    return json.dumps(resp.json())


def get_all_users():
    usersURL = f"{data_url}/getAllUsers"
    allUsers = requests.get(usersURL).json()
    return allUsers["telegramUsers"]


def get_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    user = requests.get(userURL).json()
    return user["telegramUser"]


def delete_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    user = requests.delete(userURL).json()
    return user["msg"]
