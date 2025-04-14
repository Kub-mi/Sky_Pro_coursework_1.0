import json
from datetime import datetime
from time import strptime

import pandas as pd

PATH_TO_EXCEL = "../data/operations.xlsx"

def get_greeting():
    """Возвращает приветствие в зависимости от часа входящего времени."""
    user_time_hour = datetime.now().hour
    if 5 <= user_time_hour < 12:
        return "Доброе утро"
    elif 12 <= user_time_hour < 18:
        return "Добрый день"
    elif 18 <= user_time_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_period(file_path: str, date_start: str, date_end: str):
    """
    Функция получения периода
    """
    df = pd.read_excel(file_path, sheet_name="Отчет по операциям")
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst = True)

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





def load_transactions(filepath=PATH_TO_EXCEL):
    """Загружает транзакции из Excel-файла и нормализует имена столбцов."""
    df = pd.read_excel(filepath, parse_dates=['Дата операции'])
    df.columns = [col.strip() for col in df.columns]
    return df