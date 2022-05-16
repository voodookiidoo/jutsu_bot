from bs4.element import Tag
import requests
from random import choice
from bs4 import BeautifulSoup

j_menu = r'https://jut.su/by-episodes/'
j_tech_url = 'https://jut.su/technique/{}'
HEADER = {'User-Agent': 'User-Agent Mozilla/5.0 (compatible; Yandex...)'}


def get_random_jutsu_page() -> str:
	"""Parse the jutsu page to choose random jutsu from it

	:return: an abs link to random jutsu
	"""
	page = requests.get(j_menu, headers=HEADER)
	soup = BeautifulSoup(page.text, 'html.parser')
	res = soup.findAll(name='ul', attrs={'class': 's_t_list'})
	random_episode = choice(res)
	random_jutsu_page = choice(
		[i.get('href') for i in random_episode.findAll(name='a') if i.attrs.get('title') is None])
	return random_jutsu_page


def main():
	print(get_random_jutsu_page())


# print(page.status_code)

if __name__ == '__main__':
	main()
