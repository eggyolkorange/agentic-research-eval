"""The shape of a research brief. Fixed fields make every number checkable."""
from pydantic import BaseModel, Field


class Claim(BaseModel):
    text: str = Field(description="One factual statement in the brief")
    value: float | None = Field(default=None, description="The number, if any")
    source: str = Field(description="Where it came from, e.g. 'yfinance: income statement FY2025'")


class Brief(BaseModel):
    ticker: str
    company: str
    summary: str
    claims: list[Claim]
    key_risk: str
    # TODO: add fields you want to evaluate (revenue, net income, margin, 1y return)
