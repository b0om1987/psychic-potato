from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ADAPTABLE_APP_NAME = os.getenv('EXTERNAL_URL')

# webhook settings
WEBHOOK_HOST = f'{ADAPTABLE_APP_NAME}'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=3000)
