import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

from quiz import get_question, new_quiz
from table import create_table, get_quiz_index, update_quiz_index
from questions import data as quiz_data


logging.basicConfig(level=logging.INFO)

API_TOKEN = '7089758064:AAHC1xFSsb9fOzxQmNdwKQMNJAvKXQ9e2pw'

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text=="Начать игру")
@dp.message(Command('quiz'))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз! Первый вопрос: ...")
    await new_quiz(message)

@dp.callback_query(F.data == "right_answer")
@dp.callback_query(F.data == "wrong_answer")
async def answer_cb(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    current_question_index = await get_quiz_index(callback.from_user.id)

    if callback.data == 'right_answer':
        await callback.message.answer("Верно!")
    elif callback.data == 'wrong_answer':
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())