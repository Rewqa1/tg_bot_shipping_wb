import json
import os
from datetime import datetime

from api_requests.Request import RequestWB
from utils.parse import parse_income
from utils.utils import read_json, create_incomes_excel


async def initialize():
    config = await read_json('bot/config/config.json')
    date_start = datetime.strptime(config['settings']['date_start'], '%Y-%m-%dT%H:%M:%S')
    date_end = datetime.strptime(config['settings']['date_end'], '%Y-%m-%dT%H:%M:%S')

    income_request = RequestWB(token=os.getenv('WB_TOKEN_STAT'), url=os.getenv('URL_WB_INCOMES'), params={
        'dateFrom': f'{date_start}'})
    income_response = income_request.get_data()


    income, all_income = await parse_income(income_response, date_start, date_end)

    await create_incomes_excel(income, all_income)
