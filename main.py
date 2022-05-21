import json
import requests
from handler import get_options
from parser import get_random_jutsu_page, JutsuPage, StylePage, get_all_style_pages, get_styled_page_jutsu, HEADER
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

with open('src/BOTKEY.txt', 'r') as f:
	TKN = f.read()
bot = TeleBot(TKN)


@bot.callback_query_handler(lambda call: call.data == 'main.menu')
def start_call(call: CallbackQuery):
	brd = InlineKeyboardMarkup(row_width=1)
	his = InlineKeyboardButton(text='Jutsu history', callback_data='hist.menu')
	fav = InlineKeyboardButton(text='Favorite jutsu', callback_data='fav.menu')
	new = InlineKeyboardButton(text='Learn new jutsu', callback_data='new.menu')
	brd.row(his, fav)
	brd.row(new)
	bot.send_message(call.message.chat.id, 'Okay, fellow ninja.\nWhat are you up to now?', reply_markup=brd)


@bot.message_handler(commands=['start', 'menu'])
def start(msg: Message):
	brd = InlineKeyboardMarkup(row_width=1)
	his = InlineKeyboardButton(text='Jutsu history', callback_data='hist.menu')
	fav = InlineKeyboardButton(text='Favorite jutsu', callback_data='fav.menu')
	new = InlineKeyboardButton(text='Learn new jutsu', callback_data='new.menu')
	brd.row(his, fav)
	brd.row(new)
	bot.send_message(msg.chat.id, 'Hello there, fellow ninja.\nWhat are you up to now?', reply_markup=brd)


@bot.message_handler(func=lambda x: x.data == 'main.menu')
def to_main_menu(call: CallbackQuery):
	# bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
	                              reply_markup=None)
	start(call.message)


@bot.callback_query_handler(func=lambda x: x.data.startswith('style.menu'))
def style_menu_handler(call: CallbackQuery):
	options = get_options(call.data.split('?', maxsplit=1)[1])
	if options is None:
		return
	spage = StylePage.from_link(options['link'])
	description = spage.get_description()
	brd = InlineKeyboardMarkup()
	controllers = spage.get_controllers()

	jutsu_list = get_styled_page_jutsu(requests.get(spage.link, headers=HEADER))
	for i in range(0, len(jutsu_list) - 1, 2):
		brd.row(InlineKeyboardButton(text=jutsu_list[i].name), InlineKeyboardButton(text=jutsu_list[i + 1].name))
	if len(jutsu_list) % 2 == 1:
		brd.row(InlineKeyboardButton(text=jutsu_list[-1]))

	if controllers is None or controllers.get('prev') is None:
		bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
		                              reply_markup=None)
		bot.send_message(call.message.chat.id, '<b>{}</b>\n{}'.format(spage.name, description), parse_mode="HTML",
		                 reply_markup=brd)
	else:
		if len(controllers) == 2:
			brd.row(InlineKeyboardButton(text='Назад', callback_data='style.menu?link={}'.format(options['prev'])),
			        InlineKeyboardButton(text='Далее', callback_data='style.menu?link={}'.format(options['next'])))
		else:
			cont = controllers.popitem()
			if cont[0] == 'next':
				brd.row(InlineKeyboardButton(text='Далее', callback_data='style.menu?link={}'.format(options['next'])))
			else:
				brd.row(InlineKeyboardButton(text='Назад', callback_data='style.menu?link={}'.format(options['prev'])))
		bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
		                              reply_markup=brd)


@bot.message_handler(commands=['help'])
def helper(msg: Message):
	bot.send_message(msg.chat.id, 'This bot will help you to learn a few new jutsu!\n'
	                              'The bot is completly free, the only reward i need is your attention\n'
	                              'You can check the source code of this bot on https://github.com/voodookiidoo/jutsu_bot\n'
	                              'Also check my telegram https://t.me/voodookiidoo\n'
	                              'And my VK https://vk.com/voodookiidoo', disable_web_page_preview=True, )


# TODO add the handler for favorite jutsu
@bot.callback_query_handler(func=lambda x: x.data == 'fav.menu')
def fav_jutsu_handler(callback: CallbackQuery):
	pass


@bot.callback_query_handler(func=lambda x: x.data.startswith('jutsu.?'))
def jutsu_selection_handler(call: CallbackQuery):  # handles the menu where the jutsu is already selected
	bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
	                              reply_markup=None)
	d = call.data.split('.?', maxsplit=1)[1]  # избавляемся от ненужной части data
	options = get_options(d)  # парсим нужную часть data, вытаскивая нужные параметры
	if options is None:
		jutsu = get_random_jutsu_page()
	else:
		jutsu = JutsuPage(options['link'], options['name'])
	description, *seals = jutsu.get_both()
	# print(description)

	add_to_fav = InlineKeyboardButton(text='Add to favorite', callback_data='fav.menu')
	explore_new = InlineKeyboardButton(text='Explore another jutsu', callback_data='new.menu')
	to_menu = InlineKeyboardButton(text='Get to main menu', callback_data='main.menu')
	brd = InlineKeyboardMarkup()
	for i in [add_to_fav, explore_new, to_menu]:
		brd.row(i)
	bot.send_message(call.message.chat.id, '<b>{}</b>\n{}'.format(jutsu.name, description), parse_mode='HTML')
	if not seals:
		bot.send_message(call.message.chat.id, 'No seals requiered', reply_markup=brd)
	else:
		bot.send_message(call.message.chat.id, 'Seals requiered: {}'.format(' -> '.join(seals)), reply_markup=brd)

	with open('src/history.json', 'r') as file:
		data = json.load(file)
	if data.get(call.message.from_user.id) is None:
		data[call.message.from_user.id] = {'hist': [call.message.text], 'fav': []}


# TODO add the handler for jutsu menu
@bot.callback_query_handler(func=lambda x: x.data == 'new.menu')
def new_jutsu_handler(callback: CallbackQuery):  # handles menu where you choose a jutsu
	# builds from style list and random jutsu choice button
	bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
	                              reply_markup=None)
	brd = InlineKeyboardMarkup()
	styles_list = get_all_style_pages()
	for i in range(0, len(styles_list), 3):
		first = styles_list[i]
		second = styles_list[i + 1]
		third = styles_list[i + 2]
		brd.row(*[InlineKeyboardButton(text=x.name.rstrip('Техники '),
		                               callback_data='style.menu.?link={}'.format(x.link)) for x in
		          [first, second, third]])
	rand_choice = InlineKeyboardButton(text='Choose a random jutsu', callback_data='jutsu.?NULL')

	brd.add(rand_choice)
	bot.send_message(callback.message.chat.id, 'Choose a style for new jutsu', reply_markup=brd)


# TODO add the handler for jutsu history
@bot.callback_query_handler(func=lambda x: x.data == 'hist.menu')  # handles the jutsu history menu
def jutsu_history_handler(callback: CallbackQuery):
	bot.send_message(callback.message.chat.id, 'Here will be listed the history of jutsu searched by user')


bot.polling()
