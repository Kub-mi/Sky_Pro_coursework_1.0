import json
import logging
from functools import wraps
from typing import Callable, Optional, Union
from datetime import datetime, timedelta

import pandas as pd

# Настройка логгера
logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/reports.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



def save_report(file_name: Optional[str] = None):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Запуск функции-отчета: {func.__name__}")
            result = func(*args, **kwargs)

            # По умолчанию имя файла
            target_file = file_name or f"{func.__name__}_report.json"

            # Сохраняем в JSON
            try:
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info(f"Отчет сохранен в файл: {target_file}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")

            return result

        return wrapper
    return decorator if file_name is not None else decorator(None)


# 📌 Отчет: траты по категории за 3 месяца
@save_report
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None
) -> dict:
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    # Убедимся, что "Дата операции" — datetime
    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    filtered = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= end_date)
    ]

    filtered["Сумма числом"] = (
        filtered["Сумма платежа"].astype(str).str.replace(",", ".").astype(float).abs()
    )

    total = round(filtered["Сумма числом"].sum(), 2)

    logger.info(f"Категория: {category}, Сумма трат за 3 месяца: {total}")

    return {category: total}
