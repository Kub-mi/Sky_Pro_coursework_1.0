import json
import logging
import os
from collections import defaultdict

import requests
from dotenv import load_dotenv

from src.utils import PATH_TO_EXCEL, get_correct_dates, get_greeting, get_period

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/views.log")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_user_settings(filepath="../user_settings.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


load_dotenv()


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


def main_info(date_time):
    logger.info("запуск функции main_info")
    start_date, end_date = get_correct_dates(date_time)
    sorted_df = get_period(PATH_TO_EXCEL, start_date, end_date)

    greeting = get_greeting()

    user_settings = load_user_settings()

    # Словарь для подсчёта сумм и кешбэка по каждой карте
    cards_summary = defaultdict(lambda: {"total": 0.0, "cashback": 0.0})

    for _, row in sorted_df.iterrows():
        last_digits = str(row["Номер карты"])[-4:]
        try:
            amount = abs(float(str(row["Сумма платежа"]).replace(",", ".")))
            cashback = float(
                str(row["Бонусы (включая кэшбэк)"]).replace(",", ".") or 0.0
            )
        except ValueError:
            continue

        cards_summary[last_digits]["total"] += amount
        cards_summary[last_digits]["cashback"] += cashback

    # Формируем JSON по картам
    cards_json = [
        {
            "last_digits": digits,
            "total_spent": round(data["total"], 2),
            "cashback": round(data["total"] * 0.01, 2),  # 1% кешбэк
        }
        for digits, data in cards_summary.items()
    ]

    # Топ-5 транзакций
    sorted_df["Сумма платежа числом"] = (
        sorted_df["Сумма платежа"].astype(str).str.replace(",", ".").astype(float).abs()
    )
    top_df = sorted_df.sort_values(by="Сумма платежа числом", ascending=False).head(5)

    top_transactions = []
    for _, row in top_df.iterrows():
        top_transactions.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(float(str(row["Сумма платежа"]).replace(",", ".")), 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    # Курсы валют и акции
    currency_rates = get_currency_rates(user_settings.get("user_currencies", []))
    logger.info(f"Получаем список валют и их курса{currency_rates}")

    stock_prices = get_stock_price(user_settings.get("user_stocks"))
    logger.info(f"получаем список акций и их цен {stock_prices}")

    return {
        "greeting": greeting,
        "cards": cards_json,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
