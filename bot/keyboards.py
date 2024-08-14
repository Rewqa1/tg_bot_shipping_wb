from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Запросить поставки')]
], resize_keyboard=True, input_field_placeholder='Выберите действие...')

settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить дату отчетного периода', callback_data='change_date')],
    [InlineKeyboardButton(text='Запросить отчет о поставках', callback_data='generate_incomes')]
])

