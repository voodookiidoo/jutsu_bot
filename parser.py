import typing

from bs4.element import Tag
import requests
from requests.models import Response
from random import choice
from bs4 import BeautifulSoup
from telebot import TeleBot
from typing import List, Union
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from itertools import count
import json

j_template = r'https://jut.su{}'
j_menu = r'https://jut.su/by-episodes/'
j_tech_url = r'https://jut.su/technique/{}'
HEADER = {'User-Agent': 'User-Agent Mozilla/5.0 (compatible; Yandex...)'}  # USED FOR REQURESTS, ERROR 403 IF SKIPPED


class StylePage:
	def __init__(self, link, name):
		self.__link = j_template.format(link) if not link.startswith('https') else link
		self.__name = name

	@staticmethod
	def from_link(link):
		page = requests.get(link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		res = soup.find(name='h1', attrs={'class':'b-b-title'})
		res = ''.join(filter(str.isprintable, res.text))
		return StylePage(link, res)

	def get_controllers(self):
		page = requests.get(self.link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		both = soup.find(name='div', attrs={'id': 'navigation', 'class':'ignore-select'})
		if both is None:
			return None
		refs = both.findAll('a')
		result = {}
		for value in refs:
			if value.text == 'Назад':
				result['prev'] = value.get('href')
			if value.text == 'Далее':
				result['next'] = value.get('href')
		return result

	def get_description(self):
		page = requests.get(self.link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		res = soup.find(name='div', attrs={'id': 'ujbasecont'})
		res = ''.join(filter(str.isprintable, res.text))
		return res

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

	def __hash__(self):
		return hash(self.link) + hash(self.name)

	def __eq__(self, other):
		return self.name == other.name and self.link == other.link


class JutsuPage:
	def __init__(self, link, name):
		self.__link = link
		self.__name = name

	def get_description(self) -> str:
		"""Parse the page by link, return the description as a string

		:return: description of a jutsu
		"""
		page = requests.get(self.link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		res = soup.find(name='div', attrs={'class': 'underthevkvideo', 'itemprop': 'description'})
		res = ''.join(filter(str.isprintable, res.text))
		return res

	def get_hand_seals(self) -> List[str]:
		"""Parse the page by link, return lits of hand seals as strings

		:return: hand seals as a list of strings
		"""
		page = requests.get(self.link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		res = soup.find(name='ul', attrs={'class': 'story_seals_b'})
		if res is None:
			return []
		res = res.findAll(name='a')
		res = list(map(lambda x: x.get('title'), res))
		return res

	def get_both(self) -> List[str]:
		page = requests.get(self.link, headers=HEADER)
		soup = BeautifulSoup(page.text, 'html.parser')
		res = soup.find(name='div', attrs={'class': 'underthevkvideo', 'itemprop': 'description'})
		res = ''.join(filter(str.isprintable, res.text))
		result = [res]
		seals = soup.find(name='ul', attrs={'class': 'story_seals_b'})
		if seals is None:
			return result
		seals = seals.findAll(name='a')
		seals = map(lambda x: x.get('title'), seals)
		result.extend(seals)
		return result

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


def get_all_style_pages() -> List[StylePage]:
	with open('src/tech_headers.json', 'r') as file:
		data = json.load(file)
	total = [StylePage(x['link'], x['name']) for x in data['headers']]
	return total


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
	"""Get all JutsuPage objects withing a single GET response

	:param resp: GET response object to parse JutsuPage objects
	:return: lits of JutsuPage extracted from Response object
	"""
	soup = BeautifulSoup(resp.text, 'html.parser')
	res = soup.findAll(name='div', attrs={'class': 'technicBlock'})
	data = []
	for one in res:
		one: Tag
		x = one.find(name='a')
		data.append(JutsuPage(x.get('href'), x.text))
	return data


def get_all_styled_jutsu(style: StylePage) -> List[JutsuPage]:
	"""Makes requests and returns a list of all the jutsu of a certain style

	:param style: StylePage object to request and parse requested pages
	:return: list of JutsuPage objects that belong to a certain style
	"""
	page = requests.get(style.link, headers=HEADER)
	data = get_styled_page_jutsu(page)
	for page_index in count(2, 1):
		page = requests.get('{}{}/{}/'.format(style.link, 'page', page_index), headers=HEADER)
		if page.status_code != 200:
			break
		data.extend(get_styled_page_jutsu(page))
	return data


def build_jutsu_data(bot: TeleBot, call: CallbackQuery, jutsu: JutsuPage) -> None:
	pass

def build_full_jutsu_json():
	jutsu_id = 0
	data = {}
	style_lits = get_all_style_pages()
	for style in style_lits:
		jutsu_list = get_all_styled_jutsu(style)
		for jutsu in jutsu_list:
			data[jutsu_id] = {'name':jutsu.name, 'link':jutsu.link}
			jutsu_id += 1
	with open('src/jutsu_data.json', 'w') as file:
		json.dump(data, file, indent=4)


def build_reversed_json():
	with open('src/jutsu_data.json', 'r') as file:
		data = json.load(file)
	new_data = {value["name"]: key for key, value in data.items()}
	with (open('src/jutsu_names.json', 'w')) as file:
		json.dump(new_data, file)

def main():
	page = StylePage.from_link('https://jut.su/lava/')
	print(page.get_controllers())

if __name__ == '__main__':
	main()
