"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from random import randint
import random
import asyncio
import os
import io
from time import sleep
import PIL
from PIL import Image
import concurrent.futures

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5580991208:AAE3a_B0HWZuq8Ti_wL8aqpGRJbt2kTjWBc'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def imagezz(seed):
    
    random.seed(seed)
    first_layer_image = Image.open('img/head/head_'+str(randint(1, 20))+'.png')
    second_layer_image = Image.open('img/eyes/eyes_'+str(randint(1, 20))+'.png')
    #first_layer_image = Image.open('img/head/head_'+str(3)+'.png')
    #second_layer_image = Image.open('img/eyes/eyes_'+str(1)+'.png')
    first_layer_image.paste(second_layer_image, (0,0), second_layer_image)
    img = first_layer_image
    width, height = img.size
    fc = [randint(110, 255), randint(110, 255), randint(110, 255)]
    sc = [randint(40, 100), randint(40, 100), randint(40, 100)]
    #img.putpixel((31, 31), (122, 12, 112))
    for temp1 in range(width):
        for temp2 in range(height):
            if img.getpixel((temp1, temp2)) == (255, 0, 0, 255):
                img.putpixel((temp1, temp2), (randint(fc[0]-40, fc[0]), randint(fc[1]-40, fc[1]), randint(fc[2]-40, fc[2]), 255))
                random.seed(randint(-999999, 999999))
            if img.getpixel((temp1, temp2)) == (0, 255, 0, 255):
                img.putpixel((temp1, temp2), (randint(sc[0]-10, sc[0]), randint(sc[1]-10, sc[1]), randint(sc[2]-10, sc[2]), 255))
                random.seed(randint(-999999, 999999))
    img = img.resize((1024, 1024), 0)
    return img



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm stupid!")
    

@dp.message_handler(commands=['image', 'img'])
async def image_parser(message: types.Message):
    temp = message.get_args()
    if temp:
        bityblyad = io.BytesIO()
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, imagezz, temp)
        result.save(bityblyad, format='PNG')
        bityblyad = bityblyad.getvalue()
        await message.answer_photo(bityblyad)
    else:
        await message.answer("err: No input")

    

@dp.message_handler(regexp='(^drink[s]?$|booze)')
async def cats(message: types.Message):
    with open('img/drinks/drink_' + str(randint(1, 31)) + '.jpeg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Here ya go, ausie boy.')


@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
    temp = message.get_args()
    if temp:
        await message.answer(temp)
        await message.delete()
    else:
        await message.answer("err: No input")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)