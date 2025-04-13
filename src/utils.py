from datetime import datetime
from time import strptime

import pandas as pd

PATH_TO_EXCEL = "../data/operations.xlsx"

def get_greeting(time):
    """Возвращает приветствие в зависимости от часа входящего времени."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_period(file_path: str, date_start: str, date_end: str):
    """
    Функция получения периода
    """
    df = pd.read_excel(file_path, sheet_name="Отчет по операциям")
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst = True)
    print(date_start, ' || ', date_end)

    filtered_df = df[(df['Дата операции'] >= date_start) & (df['Дата операции'] <= date_end)]
    sorted_df = filtered_df.sort_values(by = 'Дата операции')
    return sorted_df


def get_correct_dates(date_time: str):
    """
    return: '01.05.2025 15:00:00', '20.05.2025 15:00:00'
    """
    end_date = datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1)

    return start_date, end_date