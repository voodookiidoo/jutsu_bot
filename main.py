import json
import requests
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

with open('src/data.txt', 'r') as f:
	TKN = f.read()
bot = TeleBot(TKN)


@bot.message_handler(commands=['start'])
def start(msg:Message):
	brd = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	his = KeyboardButton(text='Jutsu history')
	fav = KeyboardButton(text='Favorite jutsu')
	new = KeyboardButton(text='Learn new jutsu')
	brd.add(his, fav, new)
	bot.send_message(msg.chat.id, 'Hello there, fellow ninja.\nWhat are you up to now?', reply_markup=brd)


bot.polling()