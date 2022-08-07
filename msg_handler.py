from config import *
from mongo_requests import *

def peek_stories(message):
    cid = message.chat.id
    usernames = message.text.split()
    for user in usernames:
        stories = parsing_bot.get_story(user)
        for story in stories:
            text = "User: " + user
            text += "\nStoryKey: " + story.pk
            # Try to send message to user. If it fails with telegram API error, print exception and continue
            try:
                if story.media_type == 1:
                    m_id = tg_bot.send_photo(cid, photo=story.thumbnail_url, caption=text)
                elif story.media_type == 2:
                    m_id = tg_bot.send_video(cid, video=story.video_url, caption=text)
            except telebot.apihelper.ApiTelegramException as e:
                print(e)
                print(story)
                continue