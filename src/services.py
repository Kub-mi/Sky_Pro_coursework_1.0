import logging
from collections import defaultdict
from functools import reduce

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def analyze_profitable_categories(data, year, month, cashback_rate=0.05):
    """
    Анализирует выгодность категорий по кешбэку за указанный месяц и год.

    :param data: DataFrame с транзакциями (должен содержать "Дата операции", "Сумма платежа", "Категория")
    :param year: Год анализа
    :param month: Месяц анализа
    :param cashback_rate: Процент кешбэка для расчёта (по умолчанию 5%)
    :return: Словарь (JSON) с категориями и потенциальным кешбэком
    """
    logger.info(f"Анализ выгодных категорий кешбэка за {month:02d}.{year}")

    # 1. Фильтрация транзакций по дате
    filtered_data = data[
        (data["Дата операции"].dt.year == year) &
        (data["Дата операции"].dt.month == month)
    ]

    logger.info(f"Найдено {len(filtered_data)} транзакций за период")

    # 2. Вычисление кешбэка по строкам: (категория, сумма_кешбэка)
    def extract_cashback(row):
        try:
            amount = abs(float(str(row["Сумма платежа"]).replace(",", ".")))
            category = row["Категория"]
            cashback = round(amount * cashback_rate, 2)
            return (category, cashback)
        except Exception as e:
            logger.warning(f"Ошибка при обработке строки {row}: {e}")
            return None

    cashback_list = list(filter(None, map(extract_cashback, filtered_data.to_dict("records"))))

    logger.info(f"Обработка {len(cashback_list)} строк с кешбэком")

    # 3. Агрегация кешбэка по категориям
    def accumulate(acc, item):
        category, cashback = item
        acc[category] += cashback
        return acc

    category_cashback = reduce(accumulate, cashback_list, defaultdict(float))

    logger.info("Завершён анализ кешбэка по категориям")

    # 4. Преобразуем в обычный словарь и возвращаем
    return dict(category_cashback)
