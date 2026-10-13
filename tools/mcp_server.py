"""Stretch goal: serve company data as an MCP tool.
See the MCP Python SDK quickstart (FastMCP)."""
from mcp.server.fastmcp import FastMCP

from tools.data import get_company_data

mcp = FastMCP("company-data")


@mcp.tool()
def company_data(ticker: str) -> dict:
    """Financial data for a listed company."""
    return get_company_data(ticker)


if __name__ == "__main__":
    mcp.run()
