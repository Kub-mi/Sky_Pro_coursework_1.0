from unittest.mock import patch

import pytest

from src.views import get_stock_price, get_currency_rates, main_info
import os
import logging

# Создаём директорию logs, если она не существует
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("test_views")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_views.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("API_KEY_PRICE", "test_api_key_price")
    monkeypatch.setenv("API_KEY_CURRENCY", "test_api_key_currency")

@patch("src.views.requests.get")
def test_get_stock_price(mock_get, mock_env):
    mock_response = {
        "data": [{
            "close": 157.23
        }]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    symbols = ["AAPL", "AMZN"]
    result = get_stock_price(symbols)

    assert isinstance(result, dict)
    assert "AAPL" in result
    assert result["AAPL"] == 157.23

@patch("src.views.requests.get")
def test_get_currency_rates(mock_get, mock_env):
    mock_response = {
        "success": True,
        "quotes": {
            "RUBUSD": 0.012,
            "RUBEUR": 0.0105
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = get_currency_rates(["USD", "EUR"])
    assert isinstance(result, list)
    assert {"currency": "USD", "rate": 83.3333} in result
    assert {"currency": "EUR", "rate": 95.2381} in result


@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_price")
@patch("src.views.load_user_settings")
@patch("src.views.get_period")
@patch("src.views.get_correct_dates")
@patch("src.views.get_greeting")
def test_main_info(
    mock_greeting,
    mock_dates,
    mock_period,
    mock_settings,
    mock_stock_price,
    mock_currency_rates,
):
    mock_greeting.return_value = "Добрый день"
    mock_dates.return_value = ("2025-04-01", "2025-04-15")
    mock_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    mock_stock_price.return_value = {"AAPL": 157.5, "AMZN": 128.2}
    mock_currency_rates.return_value = [
        {"currency": "USD", "rate": 0.012},
        {"currency": "EUR", "rate": 0.0105}
    ]
    import pandas as pd
    from datetime import datetime
    df = pd.DataFrame([
        {
            "Дата операции": datetime(2025, 4, 5),
            "Номер карты": "****1234",
            "Сумма платежа": "-1500,00",
            "Бонусы (включая кэшбэк)": "15",
            "Категория": "Еда",
            "Описание": "Покупка еды"
        }
    ])
    mock_period.return_value = df

    result = main_info("2025-04-15 15:00:00")

    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result