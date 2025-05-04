
from datetime import datetime
import pandas as pd

from freezegun import freeze_time

from src.utils import get_greeting, get_correct_dates, get_period, load_transactions

import os
import logging

# Создаём директорию logs, если она не существует
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("test_utils")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


@freeze_time("2025-04-10 01:00:00")
def test_get_greeting_morning():
    assert get_greeting() == "Доброй ночи"


@freeze_time("2025-04-10 09:00:00")
def test_get_greeting_morning():
    assert get_greeting() == "Доброе утро"


@freeze_time("2025-04-10 13:00:00")
def test_get_greeting_morning():
    assert get_greeting() == "Добрый день"


@freeze_time("2025-04-10 20:00:00")
def test_get_greeting_morning():
    assert get_greeting() == "Добрый вечер"


def test_get_correct_dates():
    result = get_correct_dates("2025-04-15 15:00:00")
    # assert result == (
    #     datetime(2025, 4, 1, 15, 0, 0),
    #     datetime(2025, 4, 15, 15, 0, 0)
    # )
    assert result[0] == datetime(2025, 4, 1, 0, 0, 0)
    assert result[1] == datetime(2025, 4, 15, 15, 0, 0)
    assert all(isinstance(d, datetime) for d in result)


def test_get_period(tmp_path):
    # Создаем тестовый Excel-файл
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2025-04-01", "2025-04-10", "2025-05-01"]),
        "Номер карты": ["****1234", "****5678", "****9876"],
        "Сумма платежа": [100, 200, 300]
    })
    file_path = tmp_path / "test_excel.xlsx"
    df.to_excel(file_path, sheet_name="Отчет по операциям", index=False)

    result = get_period(str(file_path), datetime(2025, 4, 1), datetime(2025, 4, 30))

    assert len(result) == 2  # только апрельские транзакции
    assert result.iloc[0]["Сумма платежа"] == 100
    assert result.iloc[1]["Сумма платежа"] == 200


def test_load_transactions(tmp_path):
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({
        "Дата операции": pd.date_range("2024-01-01", periods=3),
        "Сумма": [100, 200, 300]
    })
    df.to_excel(file_path, index=False)

    from src.utils import load_transactions
    loaded = load_transactions(file_path)
    assert "Дата операции" in loaded.columns
