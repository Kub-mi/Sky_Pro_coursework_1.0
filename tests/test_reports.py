import os
import json
import pandas as pd
import pytest
from datetime import datetime

from src.reports import spending_by_category


@pytest.fixture
def sample_df():
    data = {
        "Дата операции": [
            "2025-01-15", "2025-02-20", "2025-03-10",
            "2025-03-25", "2025-04-01", "2025-04-05"
        ],
        "Категория": ["Кафе", "Кафе", "Транспорт", "Кафе", "Кафе", "Продукты"],
        "Сумма платежа": ["-500,00", "-250,50", "-100,00", "-749,99", "-300,00", "-1000,00"]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    return df


def test_spending_by_category_with_date(tmp_path, sample_df, monkeypatch):
    # Переключаем рабочую директорию во временную для создания файла
    monkeypatch.chdir(tmp_path)

    # Выполняем функцию
    result = spending_by_category(sample_df, "Кафе", "2025-04-10")

    # Проверяем структуру результата
    assert isinstance(result, dict)
    assert "Кафе" in result

    # Проверяем корректность суммы
    expected_sum = round(500.00 + 250.50 + 749.99 + 300.00, 2)
    assert result["Кафе"] == expected_sum

    # Проверяем, что файл с результатом создан
    report_file = tmp_path / "spending_by_category_report.json"
    assert report_file.exists()

    # Проверяем содержимое файла
    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == result


def test_spending_by_category_default_date(sample_df, monkeypatch):
    # Устанавливаем текущую дату на 2025-04-10
    monkeypatch.setattr("src.reports.datetime", datetime)
    monkeypatch.setattr("src.reports.datetime.now", lambda: datetime(2025, 4, 10))

    result = spending_by_category(sample_df, "Кафе")

    expected_sum = round(500.00 + 250.50 + 749.99 + 300.00, 2)
    assert result == {"Кафе": expected_sum}
