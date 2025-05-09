import json

import pandas as pd

from src.reports import spending_by_category
from src.services import analyze_profitable_categories
from src.utils import load_transactions
from src.views import main_info

if __name__ == "__main__":
    # date_request = input('Введите дату и время конца периода отчета в формате "2018-03-20 15:30:00": ')
    date_request = "2018-03-20 15:30:00"
    result_views = main_info(date_request)

    with open("../data/views.json", "w", encoding="utf-8") as f:
        json.dump(result_views, f, ensure_ascii=False, indent=4)
    # print(f"json-ответ:\n{result_views}")

    df = load_transactions()  # Загружаем из ../data/operations.xlsx
    # year = int(input('Введите год за который надо провести анализ (в формате 2025): '))
    # month = int(input('Введите месяц за который надо провести анализ (в формате 2): '))
    result = analyze_profitable_categories(df, year=2021, month=2)
    try:
        with open("../data/services.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

    # print("Выгодные категории кешбэка:")
    # for cat, cashback in result.items():
    #     print(f"{cat}: {cashback} руб.")

    df = pd.read_excel("../data/operations.xlsx", sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    result = spending_by_category(df, "Супермаркеты", "31.12.2021")
    print(result)
