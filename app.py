import telebot
import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


API_KEY = dict(os.environ)["API_KEY"]
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Thanks for subscribing my service.")


@bot.message_handler(commands=["help"])
def send_welcome(message):
    help_msg = """
    Following are the commands which you can use:
    /help
    ipo <name of company>
    mf <category of mutual fund>
    """
    bot.reply_to(message, help_msg)
