import asyncio
import json
import os
from datetime import datetime

from dotenv import load_dotenv

from api_requests.Request import RequestWB
from utils.parse import parse_income
from utils.utils import read_json, create_incomes_excel

load_dotenv(dotenv_path='.env')
async def main():
    income_request = RequestWB(token=os.getenv('WB_TOKEN_STAT'), url=os.getenv('URL_WB_INCOMES'), params={
        'dateFrom': '2024-06-01T00:00:00'})
    income_response = income_request.get_data()

    config = await read_json('bot/config/config.json')
    date_start_str = config['settings']['date_start']
    date_end_str = config['settings']['date_end']
    date_start_object = datetime.strptime(date_start_str, '%Y-%m-%dT%H:%M:%S')
    date_end_object = datetime.strptime(date_end_str, '%Y-%m-%dT%H:%M:%S')
    income, all_income = await parse_income(income_response, date_start_object, date_end_object)
    print(json.dumps(income, indent=4, ensure_ascii=False))
    print(json.dumps(all_income, indent=4, ensure_ascii=False))

    await create_incomes_excel(income, all_income)

asyncio.run(main())
