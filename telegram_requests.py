import instabot
import telebot
from telebot import types
import time, threading, schedule
from config import *
from mongo_requests import *

@tg_bot.message_handler(commands=['start'])
def handle_start(m):
    # initalize user record in MongoDB
    cid = m.chat.id
    uid = m.from_user.id
    date = m.date
    if was_user(cid) + is_user(cid):
        db.users.update_one({"_id": str(cid)}, {"$set": {"active": True}})
        tg_bot.send_message(cid, "Мы уже знакомы, если ты хочешь перезапустить бота, используй /stop")
    else:
        db.users.insert_one({
            "_id": str(cid),
            "first_name" : m.from_user.first_name,
            "last_name" : m.from_user.last_name,
            "nickname" : m.from_user.username,
            "active": True,
            "register": date,
            "users" : [],
            "context" : "start"
        })

@tg_bot.message_handler(commands=['add_users'])
def add_users(m):
    cid = m.chat.id
    tg_bot.send_message(cid, "Для добавления: введи имя пользователя или список имен пользователей через пробел")
    set_context(cid, "add_user")

@tg_bot.message_handler(commands=['remove_users'])
def remove_users(m):
    cid = m.chat.id
    tg_bot.send_message(cid, "Для удаления: введи имя пользователя или список имен пользователей через пробел")
    set_context(cid, "remove_user")

@tg_bot.message_handler(commands=['show_users'])
def show_users(m):
    cid = m.chat.id
    tg_bot.send_message(cid, "Список пользователей: " + str(get_users(cid)))

@tg_bot.message_handler(commands=['peek_stories'])
def peek_stories(m):
    cid = m.chat.id
    users = get_users(cid)
    user_markup = types.ReplyKeyboardMarkup(True, True)
    for i in users:
        user_markup.row(i)
    tg_bot.send_message(cid, "Введи имя пользователей", reply_markup=user_markup)
    set_context(cid, "peek_stories")

@tg_bot.message_handler()
def handle_message(m):
    cid = m.chat.id
    uid = m.from_user.id
    date = m.date
    context = get_context(cid)
    print("Context: " + context)
    print("Message: " + m.text)
    if context == "add_user":
        add_user(cid, m.text.split())
        tg_bot.send_message(cid, "Users list updated: " + str(get_users(cid)))
        set_context(cid, "start")
    elif context == "remove_user":
        remove_user(cid, m.text.split())
        tg_bot.send_message(cid, "Users list updated: " + str(get_users(cid)))
        set_context(cid, "start")
    elif context == "peek_stories":
        stories = parsing_bot.load_stories(m.text.split())
        print(dir(stories[0][0]))
        for story in stories[0]:
            if story.media_type == 1:
                image = story.thumbnail_url
            elif story.media_type == 2:
                pred = story.thumbnail_url
                video = story.video_url
        # print(stories.stories)
        # tg_bot.send_message(cid, "Stories: " + str(stories.stories))
        # set_context(cid, "start")
    else:
        tg_bot.send_message(cid, "Strange context")