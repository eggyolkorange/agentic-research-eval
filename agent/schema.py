"""The shape of a research brief. Fixed fields make every number checkable."""
from pydantic import BaseModel, Field


class Fact(BaseModel):
    value: float = Field(description="The number. Revenue and net income in USD millions; price change in percent")
    period: str = Field(description="Period it covers, e.g. 'FY ending 2025-12-31' or '12 months to 2026-10-20'")
    source: str = Field(description="The data field it came from, e.g. 'income_statement: Total Revenue'")


class Brief(BaseModel):
    ticker: str
    company: str
    summary: str = Field(description="2-3 sentences using only the supplied data")
    revenue: Fact
    net_income: Fact
    price_change_1y: Fact
    key_risk: str


class Flag(BaseModel):
    claim: str = Field(description="The claim in the brief that is wrong or unsupported")
    reason: str = Field(description="Why it does not match the data")


class Review(BaseModel):
    flags: list[Flag] = Field(description="Empty if every claim matches the data")
