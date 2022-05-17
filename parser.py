from bs4.element import Tag
import requests
from requests.models import Response
from random import choice
from bs4 import BeautifulSoup
from telebot import TeleBot
from typing import List, Union
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from itertools import count

j_template = r'https://jut.su{}'
j_menu = r'https://jut.su/by-episodes/'
j_tech_url = r'https://jut.su/technique/{}'
HEADER = {'User-Agent': 'User-Agent Mozilla/5.0 (compatible; Yandex...)'}


class StylePage:
	def __init__(self, link, name):
		self.__link = j_template.format(link)
		self.__name = name

	@property
	def link(self):
		return self.__link

	@property
	def name(self):
		return self.__name

	def __str__(self):
		return f'Name: {self.name}, link: {self.link}'

	def __repr__(self):
		return self.__str__()


class JutsuPage:
	def __init__(self, link, name):
		self.__link = link
		self.__name = name

	@property
	def link(self):
		return self.__link

	@property
	def name(self):
		return self.__name

	def __str__(self):
		return f'Name: {self.name}, link: {self.link}'

	def __repr__(self):
		return self.__str__()


def get_random_jutsu_page() -> JutsuPage:
	"""Parse the jutsu page to choose random jutsu from it

	:return: a JutsuPage object with random jutsu
	"""
	page = requests.get(j_menu, headers=HEADER)
	soup = BeautifulSoup(page.text, 'html.parser')
	res = soup.findAll(name='ul', attrs={'class': 's_t_list'})
	random_episode: Tag = choice(res)
	random_jutsu_page = choice(
		[JutsuPage(i.get('href'), i.text) for i in random_episode.findAll(name='a') if i.attrs.get('title') is None])
	return random_jutsu_page


def get_styled_page_jutsu(resp: Response) -> List[JutsuPage]:
	soup = BeautifulSoup(resp.text, 'html.parser')
	res = soup.findAll(name='div', attrs={'class': 'technicBlock'})
	data = []
	for one in res:
		one: Tag
		x = one.find(name='a')
		data.append(JutsuPage(x.get('href'), x.text))
	return data


def get_all_styled_jutsu(style: StylePage) -> List[JutsuPage]:
	page = requests.get(style.link, headers=HEADER)
	data = get_styled_page_jutsu(page)
	for page_index in count(2, 1):
		page = requests.get('{}{}/{}/'.format(style.link, 'page', page_index), headers=HEADER)
		if page.status_code != 200:
			break
		data.extend(get_styled_page_jutsu(page))
	return data


def build_inline_from_list(bot: TeleBot, callback: CallbackQuery, pages: List[Union[JutsuPage, StylePage]]):
	pass


def main():
	print(*get_all_styled_jutsu(StylePage('/lava/', 'Техники лавы')), sep='\n')


if __name__ == '__main__':
	main()
