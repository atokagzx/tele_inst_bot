import telebot
import json
from pymongo import MongoClient
from instagram_requests import InstaBot

config = json.load(open('config.json'))

# Load login parameters from config.json
login = config['login']
password = config['password']
TOKEN = config['bot_token']

parsing_bot = InstaBot(login, password)
tg_bot = telebot.TeleBot(TOKEN)
mongo = MongoClient('localhost:27017')
db = mongo.b_bot