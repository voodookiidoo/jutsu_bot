import json
import requests
import telebot


def main():
	with open('src/data.txt', 'r') as f:
		TKN = f.read()
	print(TKN)

if __name__ == '__main__':
	main()
