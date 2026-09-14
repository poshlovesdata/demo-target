"""Contract tests for the ERPNext recent-order pilot exercise."""

from collections.abc import Mapping

import erpnext_orders


class FakeReadOnlyDatabase:
    """Deterministic read-only database fake that captures one SQL query."""

    def __init__(self, records: list[dict[str, object]]) -> None:
        self.records = records
        self.calls: list[tuple[str, Mapping[str, object]]] = []

    def sql(
        self, query: str, values: Mapping[str, object]
    ) -> list[dict[str, object]]:
        self.calls.append((query, values))
        return self.records


def test_read_recent_orders_queries_sales_orders_with_useful_fields_and_order(
    monkeypatch,
) -> None:
    records = [
        {
            "name": "SAL-ORD-0002",
            "customer": "Ada",
            "transaction_date": "2026-09-13",
            "status": "To Deliver and Bill",
            "grand_total": 1200,
        }
    ]
    database = FakeReadOnlyDatabase(records)
    monkeypatch.setattr(erpnext_orders, "read_only_database", database)

    result = erpnext_orders.read_recent_orders()

    assert result == records
    query, values = database.calls[0]
    normalized_query = " ".join(query.lower().split())
    assert "from `tabsales order`" in normalized_query
    for field in ("name", "customer", "transaction_date", "status", "grand_total"):
        assert field in normalized_query
    assert "order by transaction_date desc" in normalized_query
    assert "docstatus" not in normalized_query
    assert values == {"limit": 10}


def test_read_recent_orders_respects_the_requested_limit(monkeypatch) -> None:
    database = FakeReadOnlyDatabase([])
    monkeypatch.setattr(erpnext_orders, "read_only_database", database)

    erpnext_orders.read_recent_orders(limit=3)

    assert database.calls[0][1] == {"limit": 3}
