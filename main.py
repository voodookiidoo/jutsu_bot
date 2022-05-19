import json
import requests

from parser import get_random_jutsu_page, JutsuPage, StylePage
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

with open('src/data.txt', 'r') as f:
	TKN = f.read()
bot = TeleBot(TKN)


@bot.message_handler(commands=['start', 'menu'])
def start(msg: Message):
	brd = InlineKeyboardMarkup(row_width=1)
	his = InlineKeyboardButton(text='Jutsu history', callback_data='hist.menu')
	fav = InlineKeyboardButton(text='Favorite jutsu', callback_data='fav.menu')
	new = InlineKeyboardButton(text='Learn new jutsu', callback_data='new.menu')
	brd.add(his, fav, new)
	bot.send_message(msg.chat.id, 'Hello there, fellow ninja.\nWhat are you up to now?', reply_markup=brd)

@bot.message_handler(func=lambda x: x.data == 'main.menu')
def to_main_menu(call: CallbackQuery):
	bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
	                              reply_markup=None)
	start(call.message)


@bot.message_handler(commands=['help'])
def helper(msg: Message):
	bot.send_message(msg.chat.id, 'This bot will help you to learn a few new jutsu!\n'
	                              'The bot is completly free, the only reward i need is your attention\n'
	                              'You can check the source code of this bot on https://github.com/voodookiidoo/jutsu_bot\n'
	                              'Also check my telegram https://t.me/voodookiidoo\n'
	                              'And my VK https://vk.com/voodookiidoo', disable_web_page_preview=True)


# TODO add the handler for favorite jutsu
@bot.callback_query_handler(func=lambda x: x.data == 'fav.menu')
def fav_jutsu_handler(callback: CallbackQuery):
	pass


@bot.callback_query_handler(func=lambda x: x.data.startswith('selection.menu'))
def jutsu_selection_handler(call: CallbackQuery): # handles the menu where the jutsu is already selected
	d = call.data.split('.')
	jutsu = JutsuPage(call.data.split())
	bot.send_message(call.from_user.id, )
	add_to_fav = InlineKeyboardButton(text='Add to favorite', callback_data='fav.menu')
	explore_new = InlineKeyboardButton(text='Explore another jutsu', callback_data='new.menu')
	to_menu = InlineKeyboardButton(text='Get to main menu', callback_data='main.menu')
	with open('src/history.json', 'r') as file:
		data = json.dump(file)
	if data.get(call.message.from_user.id) is None:
		data[call.message.from_user.id] = {'hist':[call.message.text], 'fav':[]}



# TODO add the handler for jutsu menu
@bot.callback_query_handler(func=lambda x: x.data == 'new.menu')
def new_jutsu_handler(callback: CallbackQuery): # handles menu where you choose a jutsu
	bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
	                              reply_markup=None)
	x = get_random_jutsu_page()
	bot.send_message(callback.message.chat.id, x.link + ' ' +  x.name, disable_web_page_preview=True)
	bot.send_message(callback.message.chat.id, 'Here will be litsed the menu for all the jutsu to learn')


# TODO add the handler for jutsu history
@bot.callback_query_handler(func=lambda x: x.data == 'hist.menu') # handles the jutsu history menu
def jutsu_history_handler(callback: CallbackQuery):
	bot.send_message(callback.message.chat.id, 'Here will be listed the history of jutsu searched by user')
	bot.add_callback_query_handler()



bot.polling()
