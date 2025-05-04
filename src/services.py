import logging
from collections import defaultdict
from functools import reduce

import pandas as pd

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/services.log")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def analyze_profitable_categories(
    data: pd.DataFrame, year: int, month: int, cashback_rate=0.05
) -> dict:
    """
    Анализирует, сколько кешбэка можно было бы заработать в каждой категории
    за указанный месяц и год.
    """
    logger.info(f"Анализ кешбэка по категориям за {month:02d}.{year} начат")

    # Убедимся, что 'Дата операция' приведена к datetime
    if not pd.api.types.is_datetime64_any_dtype(data["Дата операции"]):
        logger.info("Преобразуем 'Дата операции' к datetime")
        data["Дата операции"] = pd.to_datetime(
            data["Дата операции"], dayfirst=True, errors="coerce"
        )

    # Фильтрация по дате
    filtered_data = data[
        (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
    ]
    logger.info(f"Найдено {len(filtered_data)} строк после фильтрации по дате")

    # Функция для расчета кешбэка
    def extract_cashback(row):
        try:
            amount = float(str(row["Сумма платежа"]).replace(",", "."))
            category = row["Категория"]
            cashback = abs(round(amount * cashback_rate, 2))
            return (category, cashback)
        except Exception as e:
            logger.warning(f"Ошибка в строке: {row} — {e}")
            return None

    # Применим map + filter
    cashback_entries = list(
        filter(None, map(extract_cashback, filtered_data.to_dict("records")))
    )

    logger.info(f"Обработка {len(cashback_entries)} строк с кешбэком")

    # Агрегируем по категориям
    def aggregate(acc, item):
        category, cashback = item
        acc[category] += cashback
        return acc

    aggregated = reduce(aggregate, cashback_entries, defaultdict(float))

    logger.info("Анализ категорий завершен")

    return dict(aggregated)
