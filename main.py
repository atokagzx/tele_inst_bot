#!/usr/bin/python3

from config import *
import telegram_requests

if __name__ == "__main__":
    
    while True:
        try:
            tg_bot.polling()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)