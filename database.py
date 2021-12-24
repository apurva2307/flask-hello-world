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
    headers = {"token": config("TOKEN")}
    allUsers = requests.get(usersURL, headers=headers).json()
    if "telegramUsers" in allUsers.keys():
        return allUsers["telegramUsers"]
    else:
        return json.dumps(allUsers)


def get_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    headers = {"token": config("TOKEN")}
    user = requests.get(userURL, headers=headers).json()
    if "telegramUser" in user.keys():
        return user["telegramUser"]
    else:
        return json.dumps(user)


def delete_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    headers = {"token": config("TOKEN")}
    user = requests.delete(userURL, headers=headers).json()
    if "msg" in user.keys():
        return user["msg"]
    else:
        return json.dumps(user)
