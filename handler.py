import json
import requests
from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup



def build_jutsu_menu(bot: TeleBot, jutsu_html: str) -> None:
	"""Builds an inline keyboard menu for a selected jutsu

	:param bot: bot object
	:param jutsu_html: absolute link to selected jutsu page
	:return:
	"""
