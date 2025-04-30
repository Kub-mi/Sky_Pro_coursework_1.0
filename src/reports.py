import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional

import pandas as pd

# --- Настройка логгера ---
logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
os.makedirs("../logs", exist_ok=True)
file_handler = logging.FileHandler("../logs/reports.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


# --- Декоратор ---
def save_report(func: Optional[Callable] = None, *, file_name: Optional[str] = None):
    """
    Декоратор для сохранения результата отчета в JSON-файл (в ./data).
    Использование:
        @save_report
        @save_report(file_name="my_report.json")
    """

    def decorator(inner_func: Callable):
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            logger.info(f"Запуск функции отчета: {inner_func.__name__}")
            result = inner_func(*args, **kwargs)

            os.makedirs("data", exist_ok=True)
            file = (
                file_name
                or f"{inner_func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            path = os.path.join("data", file)

            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info(f"Отчет сохранён: {path}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")
            return result

        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


# --- Функция отчета ---
@save_report  # можно использовать и: @save_report(file_name="supermarkets_q1.json")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> dict:
    """
    Возвращает сумму трат по заданной категории за последние 3 месяца от даты.

    :param transactions: DataFrame с транзакциями
    :param category: строка — название категории
    :param date: строка — дата в формате "дд.мм.гггг" (опционально)
    :return: словарь {категория: сумма трат}
    """
    logger.info(f"Анализ категории '{category}' на дату '{date}'")

    # Определяем диапазон дат
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    # Преобразование колонки даты
    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
        )

    # фильтрация по дате и категории
    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ].copy()  # ← здесь .copy()

    # безопасное добавление нового столбца
    filtered.loc[:, "Сумма числом"] = (
        filtered["Сумма платежа"].astype(str).str.replace(",", ".").astype(float).abs()
    )

    total = round(filtered["Сумма числом"].sum(), 2)
    logger.info(f"Категория: {category}, сумма за 3 месяца: {total}")

    return {category: total}
