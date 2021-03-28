# side files
from config import token
import json
import random
import test

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from sqlighter import SQLighter
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = SQLighter('db.db')
first_answer = ' '


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Ты запустил бот для подготовки к ЕГЭ')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer('Команды бота: \n'
        '/start - начать общение \n'
        '/help - команды бота')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые задания =)")


@dp.message_handler(commands=['updatename'])
async def change_name(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
        db.update_name(message.from_user.id, message.text)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_name(message.from_user.id, message.text)


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


class Form(StatesGroup):
    answer = State()


@dp.message_handler(commands=['задание'])
async def task_command(message: types.Message):
    inline_btn_1 = InlineKeyboardButton('Следующее', callback_data='change')
    inline_btn_2 = InlineKeyboardButton('Посмотреть ответ', callback_data='hint')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)

    num = random.randint(0, 6)
    with open('math-tasks.json', encoding='utf-8') as read_file:
        data = json.load(read_file)
        first_task = data['task1']['tasks'][num]['quest']
        global first_answer
        first_answer = data['task1']['tasks'][num]['ans']
    await Form.answer.set()
    await message.reply('Вот твое первое задание \n\n' + str(first_task), reply_markup=inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'hint', state=Form.answer)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, first_answer)


@dp.callback_query_handler(lambda c: c.data == 'change')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await task_command()


@dp.message_handler(state=Form.answer)
async def check_answer(message: types.Message, state: FSMContext):
    if message.text == str(first_answer):
        await message.reply('Верно')
        async with state.proxy() as data:
            data['answer'] = message.text
        await state.finish()
    else:
        await message.reply('Неверно')


@dp.message_handler(commands='task2')
async def task2_command(message: types.Message):
    with open('math-tasks.json', encoding='utf-8') as read_file:
        data = json.load(read_file)
        caption = data['task2']['tasks'][0]['caption']
        url = data['task2']['tasks'][0]['pic']
        answer = data['task2']['tasks'][0]['ans']
        with open(url, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo, caption=caption)


if __name__ == '__main__':
    executor.start_polling(dp)
