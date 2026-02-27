import telebot
import time
import threading
import os

TOKEN = 8455414161:AAGud0XufrTHToNOjsXctJlNtSz3FwIySII
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for user in message.new_chat_members:
        user_data[user.id] = {
            "join_time": time.time(),
            "videos": 0
        }
        bot.send_message(
            message.chat.id,
            f"⚠️ {user.first_name}, ৫ মিনিটের মধ্যে ৫টি ভিডিও দিন। না দিলে অটো রিমুভ করা হবে!"
        )

        threading.Thread(
            target=check_user,
            args=(message.chat.id, user.id)
        ).start()

@bot.message_handler(content_types=['video'])
def count_video(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]["videos"] += 1

def check_user(chat_id, user_id):
    time.sleep(300)  # ৫ মিনিট
    if user_id in user_data:
        if user_data[user_id]["videos"] < 5:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.unban_chat_member(chat_id, user_id)
            except:
                pass
        del user_data[user_id]

bot.infinity_polling()
