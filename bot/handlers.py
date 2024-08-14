import json
from datetime import datetime

import aiofiles
from aiogram import types, F, Router
from aiogram.dispatcher import router

from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import bot.keyboards as kb
from initialization.initialzation import initialize
from utils.utils import read_json

router = Router()

class ChangeDateState(StatesGroup):
    change_date = State()

class DownloadState(StatesGroup):
    waiting_for_file_price_article = State()
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'{message.from_user.first_name} Добро пожаловать', reply_markup=kb.main_keyboard)

@router.message(F.text == "Запросить поставки")
async def send_settings(message: Message):
    config = await read_json("bot/config/config.json")

    await message.answer(f"<b>Текущий период парса поставок</b>:<b>{datetime.strptime(config['settings']['date_start'], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')} - {datetime.strptime(config['settings']['date_end'], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')}</b>\n",
                         reply_markup=kb.settings_keyboard, parse_mode="HTML")

@router.callback_query(F.data == "change_date")
async def change_date_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChangeDateState.change_date)
    await callback.answer()
    await callback.message.answer('Введите дату начала и дату конца парса поставок\n<b>Формат: День.Месяц.Год Часы:Минуты:Секунды - День.Месяц.Год Часы:Минуты:Секунды</b>\n <b>Пример: 23.01.2024 00:00:00 - 01.02.2024 00:00:00</b>', parse_mode='HTML')
@router.message(ChangeDateState.change_date)
async def change_date(message: Message, state: FSMContext):
    config = await read_json('bot/config/config.json')

    date_range = str(message.text)
    dates = date_range.split('-')
    date_start = dates[0].strip()
    date_end = dates[1].strip()

    success = True

    try:
        date_now = datetime.now()
        date_from = datetime.strptime(date_start, "%d.%m.%Y %H:%M:%S")

        if date_from > date_now:
            await message.answer(f'{date_from.strftime("%d.%m.%Y %H:%M:%S")} еще не наступило, введите корректные данные')
            await state.clear()
            success = False
    except ValueError:
        await message.answer('Дата начала введена некорректно')
        success = False

    try:
        date_now = datetime.now()
        date_to = datetime.strptime(date_end, "%d.%m.%Y %H:%M:%S")

        if date_to > date_now:
            await message.answer(f'{date_to.strftime("%d.%m.%Y %H:%M:%S")} еще не наступило, введите корректные данные')
            await state.clear()
            success = False
    except ValueError:
        await message.answer('Дата окончания введена некорректно')
        success = False

    if success:
        if datetime.strptime(date_start, "%d.%m.%Y %H:%M:%S") >= datetime.strptime(date_end, "%d.%m.%Y %H:%M:%S"):
            await message.answer('Дата начала должна меньше даты окончания')
            await state.clear()
        else:
            date_start = datetime.strptime(date_start, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
            date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
            config['settings']['date_start'] = date_start
            config['settings']['date_end'] = date_end
            config_data = json.dumps(config, indent=4)
            async with aiofiles.open('bot/config/config.json', 'w') as config_json:
                await config_json.write(config_data)
            await message.answer('Дата успешно обновлена\n'
                                 f'Текущий период парса поставок: {datetime.strptime(config["settings"]["date_start"], "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")} - {datetime.strptime(config["settings"]["date_end"], "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")}')
    else:
        await state.clear()

@router.callback_query(F.data == "generate_incomes")
async def generate_incomes(callback: CallbackQuery):
    await callback.answer('Запрос обрабатывается')
    await initialize()
    await callback.message.answer_document(
        document=types.FSInputFile(
            path="excel_files/Поставки.xlsx"
        )
    )