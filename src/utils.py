import requests
import json
import logging
import os
from datetime import datetime

import pandas as pd
from pandas import DataFrame

PATH_TO_EXCEL = "../data/operations.xlsx"

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

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


def get_period(file_path: str, date_start: str, date_end: str) -> DataFrame:
    """
    Функция получения периода
    """
    df = pd.read_excel(file_path, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Дата операции"] >= date_start) & (df["Дата операции"] <= date_end)
    ]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_correct_dates(date_time: str):
    """
    return: '01.05.2025 15:00:00', '20.05.2025 15:00:00'
    """
    end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1)

    return start_date, end_date


def load_transactions(filepath=PATH_TO_EXCEL):
    """Загружает транзакции из Excel-файла и нормализует имена столбцов."""
    df = pd.read_excel(filepath)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")

    df.columns = [col.strip() for col in df.columns]
    return df


def load_user_settings(filepath="../user_settings.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_stock_price(symbols):
    logger.info("запуск функции get_stock_price")
    api_key = os.getenv("API_KEY_PRICE")
    if not api_key:
        raise ValueError("API_KEY_PRICE не задан в переменных окружения")

    results = {}  # теперь это словарь

    for symbol in symbols:
        url = "http://api.marketstack.com/v2/eod"
        params = {"access_key": api_key, "symbols": symbol, "limit": 1}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info("получение данных по апи ключу")

            if data.get("data"):
                latest = data["data"][0]
                logger.info("получаем data")

                results[symbol] = round(latest.get("close", 0.0), 2)
                logger.info(f"забираем close, {results[symbol]}")

            else:
                results[symbol] = 0
                logger.info("не получилось забрать close")

        except Exception as e:
            logger.error(f"Ошибка при получении цены для {symbol}: {e}")
            print(f"Ошибка при получении цены для {symbol}: {e}")
            results[symbol] = None

    return results


def get_currency_rates(currencies, base="RUB"):
    logger.info("запуск функции get_currency_rates")
    api_key = os.getenv("API_KEY_CURRENCY")
    if not api_key:
        logger.info("API_KEY_CURRENCY не задан в переменных окружения")
        raise ValueError("API_KEY_CURRENCY не задан в переменных окружения")

    symbols = ",".join(currencies)
    logger.info("Разделяем валюты запятой для запроса сразу двух валют")

    url = f"http://api.currencylayer.com/live?access_key={api_key}&source={base}&currencies={symbols}"
    logger.info("Создаем запрос через API")

    try:
        logger.info("Отправляем запрос к API currencylayer")
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        logger.debug(f"Ответ от API: {data}")

        if not data.get("success"):
            error_info = data.get("error", {})
            logger.error(f"Ошибка от API: {error_info}")
            raise Exception(f"CurrencyLayer API Error: {error_info}")

        quotes = data.get("quotes", {})
        result = []

        for currency in currencies:
            key = f"{base}{currency}"
            rate = quotes.get(key)
            logger.info(f"Обрабатываем {key}: {rate}")

            result.append(
                {"currency": currency, "rate": round(rate, 4) if rate else None}
            )

        return result

    except Exception as e:
        print(f"Ошибка при получении курса валют: {e}")
        logger.error(f"Ошибка при получении курса валют: {e}, возвращаем: 'rate': None")
        return [{"currency": c, "rate": None} for c in currencies]


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame и возвращает список карт с расходаами
    :param sorted_df:
    :return:
    """
    pass