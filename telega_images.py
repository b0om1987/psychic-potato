import logging
from random import randint
import random
import os
import io
import asyncio
from time import sleep
import PIL
from PIL import Image
import concurrent.futures
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from config import bot, dp, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT



def imagezz(seed):
	random.seed(seed)
	first_layer_image = Image.open('img/head/head_' + str(randint(1, 20)) + '.png')
	second_layer_image = Image.open('img/eyes/eyes_' + str(randint(1, 20)) + '.png')
	first_layer_image.paste(second_layer_image, (0, 0), second_layer_image)
	img = first_layer_image
	width, height = img.size
	fc = [randint(110, 255), randint(110, 255), randint(110, 255)]
	sc = [randint(30, 100), randint(30, 100), randint(30, 100)]
	for temp1 in range(width):
		for temp2 in range(height):
			if img.getpixel((temp1, temp2)) == (255, 0, 0, 255):
				img.putpixel(
				(temp1, temp2),
				(randint(fc[0]-40, fc[0]),
				randint(fc[1]-40, fc[1]),
				randint(fc[2]-40, fc[2]),
				255)
				)
				random.seed(randint(-999999, 999999))
			if img.getpixel((temp1, temp2)) == (0, 255, 0, 255):
				img.putpixel(
				(temp1, temp2),
				(randint(sc[0]-40, sc[0]),
				randint(sc[1]-40, sc[1]),
				randint(sc[2]-40, sc[2]),
				255)
				)
				random.seed(randint(-999999, 999999))
	img = img.resize((1024, 1024), 0)
	return img


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.reply("Hi!\nDescription of the bot here.")
	

@dp.message_handler(commands=['image', 'img'])
async def image_parser(message: types.Message):
	msgarg = message.get_args()
	if msgarg:
		seed = msgarg
	else: 
		seed = None
	bity = io.BytesIO()
	loop = asyncio.get_running_loop()
	with concurrent.futures.ThreadPoolExecutor() as pool:
		result = await loop.run_in_executor(
		pool, imagezz, seed)
	result.save(bity, format='PNG')
	bity = bity.getvalue()
	await message.answer_photo(bity)
	
		
@dp.message_handler(regexp='(^drink[s]?$|booze)')
async def booze(message: types.Message):
	with open('img/drinks/drink_' + str(randint(1, 31)) + '.jpeg', 'rb') as photo:
		await message.reply_photo(photo, caption = 'Here ya go, ausie boy.')
		
		
@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
	msgarg = message.get_args()
	if msgarg:
		await message.answer(msgarg)
		await message.delete()
	else:
		await message.answer('err: No input')
		

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
