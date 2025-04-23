import logging
from collections import defaultdict

from dotenv import load_dotenv

from src.utils import PATH_TO_EXCEL, get_correct_dates, get_greeting, get_period, get_currency_rates, get_stock_price, \
    load_user_settings

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/views.log")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv()




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
