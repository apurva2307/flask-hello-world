import requests, json, pickle
from decouple import config
from database import get_all_users
from services import get_stk_recos

API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"


def sendFile(chat_id, type, file_path, file_name):
    url = f"{API_URL}/send"
    payload = {"chat_id": chat_id}
    if type == "txt":
        url = f"{url}Document"
        files = [
            (
                "document",
                (
                    f"{file_name}",
                    open(f"{file_path}", "rb"),
                    "text/plain",
                ),
            )
        ]
    resp = requests.request("POST", url, data=payload, files=files)
    return json.dumps(resp.json())


def broadcast_all(func, chat_ids, *args):
    for chat_id in chat_ids:
        func(chat_id, *args)


def broadcast_msg(chat_id, msg):
    to_url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    resp = requests.post(to_url, json=payload)
    return json.dumps(resp.json())


def broadcast_to_admin(msg):
    to_url = f"{API_URL}/sendMessage"
    payload = {"chat_id": 44114772, "text": msg, "parse_mode": "HTML"}
    resp = requests.post(to_url, json=payload)
    return json.dumps(resp.json())


def broadcast_items(chat_id, item, type):
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
        txt = req["message"]["text"]
        # pickle.dumps(txt)
    elif "sticker" in req["message"].keys():
        txt = req["message"]["sticker"]["file_id"]
    elif "document" in req["message"].keys():
        txt = req["message"]["document"]["file_id"]
    elif "photo" in req["message"].keys():
        txt = req["message"]["photo"][0]["file_id"]
    first_name = req["message"]["chat"]["first_name"]
    username = req["message"]["chat"]["username"]
    return chat_id, txt, first_name, username


def is_command(txt):
    return txt[0] == "/"


def execute_command(command, chat_id):
    command = command.lower()
    if command == "/ipo":
        broadcast_msg(chat_id, "HI, welcome in world of IPOs..")
    elif command == "/reco":
        reco = get_stk_recos()
        broadcast_msg(chat_id, reco)
    elif command == "/help":
        help_msg = "<pre>Following are the options:</pre>"
        broadcast_msg(chat_id, help_msg)
    elif (
        command[:5].lower() == "/all "
        and chat_id == 44114772
        and command[5:8].lower() == "img"
    ):
        data = {"type": "image"}
        with open("img.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif (
        command[:5].lower() == "/all "
        and chat_id == 44114772
        and command[5:9].lower() == "file"
    ):
        data = {"type": "file"}
        with open("file.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif command[:5] == "/all " and chat_id == 44114772:
        msg = command[5:]
        broadcastToAll(msg)
    else:
        broadcast_msg(chat_id, "No such command exists..")


def broadcastToAll(msg):
    users = get_all_users()
    try:
        for user in users:
            if user["chatId"] != "44114772":
                broadcast_msg(user["chatId"], msg)
    except:
        broadcast_msg(44114772, "Some error ocurred.")
