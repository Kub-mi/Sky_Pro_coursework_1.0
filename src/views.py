# import json
# import requests
# import datetime
# import logging
# import pandas as pd
# from flask import Flask, request, jsonify
#
# # Настройка логирования
# logger = logging.getLogger("views")
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler("logs/views.log")
# file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)
#
#
# # Загрузка пользовательских настроек
# with open('/Users/mihailkubrak/Desktop/учеба/Программирование/Sky_Pro_coursework_1.0/data/user_settings.json', 'r', encoding='utf-8') as f:
#     user_settings = json.load(f)
#
# CURRENCIES = user_settings.get("user_currencies", [])
# STOCKS = user_settings.get("user_stocks", [])
#
# app = Flask(__name__)
#
#
# def get_greeting(hour):
#     """Определяет приветствие в зависимости от времени суток."""
#     if 5 <= hour < 12:
#         return "Доброе утро"
#     elif 12 <= hour < 18:
#         return "Добрый день"
#     elif 18 <= hour < 23:
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"
#
#
# def get_currency_rates():
#     """Получает текущие курсы валют."""
#     rates = []
#     for currency in CURRENCIES:
#         response = requests.get(f'https://api.exchangerate-api.com/v4/latest/RUB')
#         if response.status_code == 200:
#             data = response.json()
#             rate = data['rates'].get(currency)
#             if rate:
#                 rates.append({"currency": currency, "rate": round(rate, 2)})
#     return rates
#
#
# def get_stock_prices():
#     """Получает актуальные цены на акции."""
#     stocks = []
#     for stock in STOCKS:
#         response = requests.get(f'https://finnhub.io/api/v1/quote?symbol={stock}&token=YOUR_API_KEY')
#         if response.status_code == 200:
#             data = response.json()
#             stocks.append({"stock": stock, "price": round(data.get('c', 0), 2)})
#     return stocks
#
#
# def analyze_transactions(date_str):
#     """Анализирует транзакции за текущий месяц и вычисляет кешбэк."""
#     date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#     start_date = date.replace(day=1).strftime("%Y-%m-%d")
#     end_date = date.strftime("%Y-%m-%d")
#
#     # Загрузка данных о транзакциях
#     df = pd.read_csv("transactions.csv")
#     df["date"] = pd.to_datetime(df["date"])
#     df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
#
#     # Группировка по картам
#     cards_summary = df.groupby("card_number")["amount"].sum().reset_index()
#     cards_data = [{
#         "last_digits": str(int(row["card_number"]))[-4:],
#         "total_spent": round(row["amount"], 2),
#         "cashback": round(row["amount"] * 0.01, 2)  # 1% кешбэка
#     } for _, row in cards_summary.iterrows()]
#
#     # Топ-5 транзакций по сумме платежа
#     top_transactions = df.nlargest(5, "amount")[["date", "amount", "category", "description"]]
#     top_transactions_data = top_transactions.to_dict(orient="records")
#
#     return cards_data, top_transactions_data
#
#
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     """Обрабатывает API-запрос и возвращает JSON-ответ с данными."""
#     date_str = request.args.get('date')
#     if not date_str:
#         return jsonify({"error": "Дата не указана"}), 400
#
#     try:
#         date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#     except ValueError:
#         return jsonify({"error": "Неверный формат даты"}), 400
#
#     # Генерация JSON-ответа
#     greeting = get_greeting(date_obj.hour)
#     cards, top_transactions = analyze_transactions(date_str)
#     currency_rates = get_currency_rates()
#     stock_prices = get_stock_prices()
#
#     response = {
#         "greeting": greeting,
#         "cards": cards,
#         "top_transactions": top_transactions,
#         "currency_rates": currency_rates,
#         "stock_prices": stock_prices
#     }
#
#     return jsonify(response)



# import json
# import logging
# import os
#
# import pandas as pd
# import requests
#
# from datetime import datetime

# path_file = "/Users/mihailkubrak/Desktop/учеба/Программирование/Sky_Pro_coursework_1.0"
#
# with open(f'{path_file}/user_settings.json', 'r', encoding='utf-8') as f:
#     user_settings = json.load(f)
#
# CURRENCIES = user_settings.get("user_currencies", [])
# STOCKS = user_settings.get("user_stocks", [])

# def load_user_settings(filepath='user_settings.json'):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         return json.load(f)
#
# def get_date(my_date: str) -> datetime:
#     """Преобразует строку даты в объект datetime."""
#     try:
#         if my_date.endswith("Z"):  # Убираем 'Z', если присутствует
#             my_date = my_date[:-1]
#         return datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S")
#     except ValueError:
#         return datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
#
#
# def load_transactions(filepath='my_operations_may.xlsx'):
#     df = pd.read_excel(filepath, parse_dates=['Дата операции'])
#     df.columns = [col.strip() for col in df.columns]
#     return df
#
#
# def get_greeting(hour):
#     """Определяет приветствие в зависимости от времени суток."""
#     if 5 <= hour < 12:
#         return "Доброе утро"
#     elif 12 <= hour < 18:
#         return "Добрый день"
#     elif 18 <= hour < 23:
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"


# def get_currency_rates():
#     """Получает текущие курсы валют."""
#     rates = []
#     api_key = os.getenv("API_KEY")
#     url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/RUB'
#     headers = {"apikey": api_key}
#     for currency in CURRENCIES:
#         # response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/latest/RUB')
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             rate = data['rates'].get('conversion_rates').get(currency)
#             if rate:
#                 rates.append({"currency": currency, "rate": round(rate, 2)})
#             else:
#                 logging.warning(f"Курс для валюты {currency} не найден в ответе API.")
#         else:
#             logging.error(f"Не удалось получить курс валют. Код ответа: {response.status_code}. Ответ: {response.text}")
#         return rates

import pandas as pd
import datetime
import json
import requests
from collections import defaultdict

# === Функция генерации приветствия по времени суток ===
def get_greeting(time: datetime.datetime) -> str:
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

# === Загрузка пользовательских настроек: валюты и акции ===
def load_user_settings(filepath='/Users/mihailkubrak/Desktop/учеба/Программирование/Sky_Pro_coursework_1.0/user_settings.json'):
    """Загружает настройки пользователя из JSON-файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# === Загрузка и предобработка транзакций из Excel ===
def load_transactions(filepath='/Users/mihailkubrak/Desktop/учеба/Программирование/Sky_Pro_coursework_1.0/'
                               'data/my_operations_may.xlsx'):
    """Загружает транзакции из Excel-файла и нормализует имена столбцов."""
    df = pd.read_excel(filepath, parse_dates=['Дата операции'])
    df.columns = [col.strip() for col in df.columns]
    return df

# === Получение курсов валют с API (пример: exchangerate.host) ===
# def get_currency_rates(currencies):
#     """
#     Получает курсы валют к рублю из публичного API.
#     Курсы возвращаются в формате: {"currency": "USD", "rate": 73.21}
#     """
#     rates = []
#     for currency in currencies:
#         response = requests.get(f'https://v6.exchangerate-api.com/v6/9c8ac44f5f21f50cdaa50d95/latest/{currency}')
#         data = response.json()
#         if 'rates' in data and currency in data['rates']:
#             # Обратное значение, т.к. API отдаёт 1 RUB = X USD
#             rates.append({
#                 "currency": currency,
#                 "rate": round(1 / data['rates'][currency], 2)
#             })
#     return rates

# === Получение цен акций с API Yahoo Finance ===
# def get_stock_prices(stocks):
#     """
#     Получает цены акций с Yahoo Finance.
#     Возвращает список словарей с ценой каждой акции.
#     """
#     prices = []
#     for stock in stocks:
#         response = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={stock}')
#         data = response.json()
#         if 'quoteResponse' in data and data['quoteResponse']['result']:
#             quote = data['quoteResponse']['result'][0]
#             prices.append({
#                 "stock": stock,
#                 "price": round(quote['regularMarketPrice'], 2)
#             })
#     return prices

# === Главная функция: генерация JSON-ответа по дате ===
def generate_json_response(input_datetime_str: str) -> dict:
    """
    Главная функция: принимает строку с датой и временем, анализирует транзакции,
    формирует JSON-ответ со статистикой и данными с внешних API.
    """
    # Преобразуем строку в datetime
    input_datetime = datetime.datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    from_date = input_datetime.replace(day=1)  # начало месяца
    to_date = input_datetime  # текущая дата

    greeting = get_greeting(input_datetime)  # Генерация приветствия

    user_settings = load_user_settings()  # Валюты и акции
    df = load_transactions()  # Загружаем транзакции

    # Фильтруем операции по дате
    df_filtered = df[(df['Дата операции'] >= from_date) & (df['Дата операции'] <= to_date)]

    # Словарь для подсчёта сумм и кешбэка по каждой карте
    cards_summary = defaultdict(lambda: {'total': 0.0, 'cashback': 0.0})

    # Суммируем расходы и кешбэк по последним 4 цифрам карт
    for _, row in df_filtered.iterrows():
        card = str(row['Номер карты'])[-4:]  # последние 4 цифры
        amount = str(row['Сумма платежа']).replace(",", ".")
        cashback = str(row['Бонусы (включая кэшбэк)']).replace(",", ".") or "0.0"
        try:
            cards_summary[card]['total'] += abs(float(amount))
            cards_summary[card]['cashback'] += float(cashback)
        except ValueError:
            continue  # Пропустить ошибочные строки

    # Преобразуем словарь в список для JSON-ответа
    cards_json = [
        {
            "last_digits": digits,
            "total_spent": round(data['total'], 2),
            "cashback": round(data['total'] * 0.01, 2)  # 1% кешбэка от суммы
        }
        for digits, data in cards_summary.items()
    ]

    # Добавляем вспомогательный столбец для сортировки транзакций
    df_filtered['Сумма платежа (чистая)'] = (
        df_filtered['Сумма платежа'].astype(str).str.replace(",", ".").astype(float).abs()
    )

    # Топ-5 транзакций по сумме
    top_tx = df_filtered.sort_values(by='Сумма платежа (чистая)', ascending=False).head(5)
    top_transactions = []
    for _, row in top_tx.iterrows():
        top_transactions.append({
            "date": row['Дата операции'].strftime("%d.%m.%Y"),
            "amount": round(float(str(row['Сумма платежа']).replace(",", ".")), 2),
            "category": row['Категория'],
            "description": row['Описание']
        })

    # Получаем курсы валют и цены акций
    currency_rates = get_currency_rates(user_settings.get("user_currencies", []))
    stock_prices = get_stock_prices(user_settings.get("user_stocks", []))

    # Финальный JSON-ответ
    return {
        "greeting": greeting,
        "cards": cards_json,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }


if __name__ == "__main__":
    result = generate_json_response("2025-03-31 19:41:16")
    print(json.dumps(result, indent=2, ensure_ascii=False))
