from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from config import token
import random
import json

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
first_answer = ''
answers = []


class Form(StatesGroup):
    exc1 = State()
    exc2 = State()
    exc3 = State()
    exc4 = State()
    exc5 = State()
    exc6 = State()
    exc7 = State()
    exc8 = State()
    exc9 = State()
    exc10 = State()
    exc11 = State()
    exc12 = State()


async def write_state(stage, message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[stage] = message.text
    await message.reply('Твой ответ: ' + data[stage])


async def text_task(target, message: types.Message):
    num = random.randint(0, 5)
    with open('math-tasks.json', encoding='utf-8') as read_file:
        data = json.load(read_file)
        task = data[target]['tasks'][num]['quest']
        answer = data[target]['tasks'][num]['ans']
        answers.append(answer)
    await message.reply(task)


async def task_picture(target, message: types.Message):
    num = random.randint(0, 5)
    with open('math-tasks.json', encoding='utf-8') as read_file:
        data = json.load(read_file)
        caption = data[target]['tasks'][num]['quest']
        answer = data[target]['tasks'][num]['ans']
        pic = data[target]['tasks'][num]['pic']
        answers.append(answer)
    with open(pic, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo, caption=caption)


async def photo_task(target, message: types.Message):
    num = random.randint(0, 1)
    with open('math-tasks.json', encoding='utf-8') as read_file:
        data = json.load(read_file)
        answer = data[target]['tasks'][num]['ans']
        pic = data[target]['tasks'][num]['pic']
        answers.append(answer)
    with open(pic, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(commands="math")
async def start_command(message: types.Message):
    await message.reply('Ты начал новый вариант. Будь внимательней!')
    await Form.exc1.set()
    await text_task('task1', message)


@dp.message_handler(state='*', commands="cancel")
async def cancel_command(message: types.Message, state: FSMContext):
    await message.reply('Вариант завершен')
    await state.finish()


@dp.message_handler(state=Form.exc1)
async def get_message(message: types.Message, state: FSMContext):
    await write_state('exc1', message, state)
    await Form.next()
    await task_picture('task2', message)


@dp.message_handler(state=Form.exc2)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc2', message, state)
    await Form.next()
    await task_picture('task3', message)


@dp.message_handler(state=Form.exc3)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc3', message, state)
    await Form.next()
    await text_task('task4', message)


@dp.message_handler(state=Form.exc4)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc4', message, state)
    await Form.next()
    await photo_task('task5', message)


@dp.message_handler(state=Form.exc5)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc5', message, state)
    await Form.next()
    await photo_task('task6', message)


@dp.message_handler(state=Form.exc6)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc6', message, state)
    await Form.next()
    await photo_task('task7', message)


@dp.message_handler(state=Form.exc7)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc7', message, state)
    await Form.next()
    await photo_task('task8', message)


@dp.message_handler(state=Form.exc8)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc8', message, state)
    await Form.next()
    await photo_task('task9', message)


@dp.message_handler(state=Form.exc9)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc9', message, state)
    await Form.next()
    await photo_task('task10', message)


@dp.message_handler(state=Form.exc10)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc10', message, state)
    await Form.next()
    await text_task('task11', message)


@dp.message_handler(state=Form.exc11)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc11', message, state)
    await Form.next()
    await photo_task('task12', message)


@dp.message_handler(state=Form.exc12)
async def task_two(message: types.Message, state: FSMContext):
    await write_state('exc12', message, state)
    # await Form.next()
    await message.answer('Вариант завершен')
    await count_answer(message, state)

score = 0


async def check_answer(r_answer, stage, state: FSMContext):
    async with state.proxy() as data:
        u_answer = data[stage]
    if u_answer == str(r_answer):
        global score
        score += 1


# @dp.message_handler(state=Form.exc12)
async def count_answer(message: types.Message, state: FSMContext):
    await check_answer(answers[0], 'exc1', state)
    await check_answer(answers[1], 'exc2', state)
    await check_answer(answers[2], 'exc3', state)
    await check_answer(answers[3], 'exc4', state)
    await check_answer(answers[4], 'exc5', state)
    await check_answer(answers[5], 'exc6', state)
    await check_answer(answers[6], 'exc7', state)
    await check_answer(answers[7], 'exc8', state)
    await check_answer(answers[8], 'exc9', state)
    await check_answer(answers[9], 'exc10', state)
    await check_answer(answers[10], 'exc11', state)
    await check_answer(answers[11], 'exc12', state)
    global score
    # await bot.send_message(message.from_user.id, str(score))
    await message.answer("Твой результат - " + str(score) + "/12")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
