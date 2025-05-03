import json
import pandas as pd
import pytest
from freezegun import freeze_time
from pathlib import Path


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
    monkeypatch.chdir(tmp_path)

    result = spending_by_category(sample_df, "Кафе", "10.04.2025")
    assert isinstance(result, dict)
    assert "Кафе" in result

    expected_sum = round(500.00 + 250.50 + 749.99 + 300.00, 2)
    assert result["Кафе"] == expected_sum

    report_file = Path("data") / "spending_by_category_report.json"
    assert report_file.exists()

    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == result


@freeze_time("2025-04-10")
def test_spending_by_category_default_date(sample_df):
    result = spending_by_category(sample_df, "Кафе")

    expected_sum = round(500.00 + 250.50 + 749.99 + 300.00, 2)
    assert result == {"Кафе": expected_sum}
