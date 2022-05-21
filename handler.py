import json
import requests
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union

def get_options(opt_str: str) -> Union[dict, None]:
	result = {}
	if '=' not in opt_str:
		return None
	data = opt_str.split('&')
	for pair in data:
		x = pair.split('=')
		result[x[0]] = x[1]
	return result

def main():
	print(get_options('name=Техника летящего бога грома&link=https://among_us'))

if __name__ == '__main__':
	main()