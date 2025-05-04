import pandas as pd
from datetime import datetime
from src.services import analyze_profitable_categories

def test_analyze_profitable_categories():
    data = pd.DataFrame([
        {"Дата операции": datetime(2023, 3, 5), "Сумма платежа": "-1000", "Категория": "Еда"},
        {"Дата операции": datetime(2023, 3, 10), "Сумма платежа": "-2000", "Категория": "Еда"},
        {"Дата операции": datetime(2023, 3, 15), "Сумма платежа": "-1500", "Категория": "Транспорт"},
        {"Дата операции": datetime(2023, 4, 1), "Сумма платежа": "-500", "Категория": "Одежда"},
    ])

    result = analyze_profitable_categories(data, 2023, 3)
    assert result == {
        "Еда": round((1000 + 2000) * 0.05, 2),
        "Транспорт": round(1500 * 0.05, 2),
    }
