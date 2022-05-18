import json
import requests
from parser import get_random_jutsu_page
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

with open('src/data.txt', 'r') as f:
	TKN = f.read()
bot = TeleBot(TKN)


@bot.message_handler(commands=['start', 'menu'])
def start(msg: Message):
	brd = InlineKeyboardMarkup(row_width=1)
	his = InlineKeyboardButton(text='Jutsu history', callback_data='jutsu_history')
	fav = InlineKeyboardButton(text='Favorite jutsu', callback_data='fav_jutsu')
	new = InlineKeyboardButton(text='Learn new jutsu', callback_data='new_jutsu')
	brd.add(his, fav, new)
	bot.send_message(msg.chat.id, 'Hello there, fellow ninja.\nWhat are you up to now?', reply_markup=brd)


@bot.message_handler(commands=['help'])
def helper(msg: Message):
	bot.send_message(msg.chat.id, 'This bot will help you to learn a few new jutsu!\n'
	                              'The bot is completly free, the only reward i need is your attention\n'
	                              'You can check the source code of this bot on https://github.com/voodookiidoo/jutsu_bot\n'
	                              'Also check my telegram https://t.me/voodookiidoo\n'
	                              'And my VK https://vk.com/voodookiidoo', disable_web_page_preview=True)


# TODO add the handler for favorite jutsu
@bot.callback_query_handler(func=lambda x: x.data == 'fav_jutsu')
def fav_jutsu_handler(callback: CallbackQuery):
	bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
	                              reply_markup=None)
	bot.send_message(callback.from_user.id, 'Here will be listed the favourite jutsu of user')


# TODO add the handler for jutsu menu
@bot.callback_query_handler(func=lambda x: x.data == 'new_jutsu')
def new_jutsu_handler(callback: CallbackQuery):
	bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
	                              reply_markup=None)
	x = get_random_jutsu_page()
	bot.send_message(callback.message.chat.id, x.link + ' ' +  x.name, disable_web_page_preview=True)
	bot.send_message(callback.message.chat.id, 'Here will be litsed the menu for all the jutsu to learn')


# TODO add the handler for jutsu history
@bot.callback_query_handler(func=lambda x: x.data == 'jutsu_history')
def jutsu_history_handler(callback: CallbackQuery):
	bot.send_message(callback.message.chat.id, 'Here will be listed the history of jutsu searched by user')


bot.polling()
