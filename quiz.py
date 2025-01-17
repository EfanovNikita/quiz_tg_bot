from table import get_quiz_index, update_quiz_index_and_points
from questions import data as quiz_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_points = 0
    await update_quiz_index_and_points(user_id, current_question_index, current_points)
    
    await get_question(message, user_id)

async def get_question(message, user_id):

    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for i, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"right_answer {i}" if option == right_answer else f"wrong_answer {i}")
        )

    builder.adjust(1)
    return builder.as_markup()
