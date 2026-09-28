from pydantic import BaseModel


class FieldValue(BaseModel):
    value: str | None
    quote: str | None
    page: int | None


class Invoice(BaseModel):
    vendor: FieldValue
    invoice_number: FieldValue
    date: FieldValue
    currency: FieldValue
    total: FieldValue
