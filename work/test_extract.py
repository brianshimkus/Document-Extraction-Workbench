import json
from pathlib import Path
import pytest
from contracts import Invoice
from extract import normalize, validate_record, read_pages


def test_invalid_calendar_date():
    with pytest.raises(ValueError):
        normalize("date", "2026-02-30")


@pytest.mark.parametrize("value", ["NaN", "-1.00", "12.345"])
def test_invalid_amount(value):
    with pytest.raises(ValueError):
        normalize("total", value)


def test_missing_currency_is_not_guessed():
    assert normalize("currency", None) is None


def test_false_quote_is_flagged():
    raw = json.loads(Path("data/mock/invoice-01.json").read_text())
    raw["total"]["quote"] = "Total: 999.00"
    invoice = Invoice.model_validate(raw)
    result = validate_record(invoice, read_pages("data/documents/invoice-01.txt"))
    assert "total: quote not found on page" in result["issues"]


def test_plausible_wrong_value_can_pass_simple_validation():
    invoice = Invoice.model_validate_json(Path("data/mock/invoice-03.json").read_text())
    result = validate_record(invoice, read_pages("data/documents/invoice-03.txt"))
    assert result["values"]["total"] == "9.00"
    assert result["needs_review"] is False  # This is a documented blind spot.


def test_vision_requires_review():
    invoice = Invoice.model_validate_json(Path("data/mock/invoice-01.json").read_text())
    assert validate_record(invoice, [""], vision=True)["needs_review"]
