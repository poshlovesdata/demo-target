"""Independent contract tests for the ERPNext customer intake exercise."""

from collections.abc import Mapping

import erpnext_customers


class FakeReadOnlyDatabase:
    """Deterministic SQL fake that records every requested read query."""

    def __init__(self, records: list[dict[str, object]]) -> None:
        self.records = records
        self.calls: list[tuple[str, Mapping[str, object]]] = []

    def sql(
        self, query: str, values: Mapping[str, object]
    ) -> list[dict[str, object]]:
        self.calls.append((query, values))
        return self.records


def test_read_recent_customers_queries_recent_customer_records(monkeypatch) -> None:
    records = [
        {
            "name": "CUST-0002",
            "customer_name": "Ada Lovelace",
            "customer_group": "Commercial",
            "territory": "Nigeria",
            "disabled": 0,
        }
    ]
    database = FakeReadOnlyDatabase(records)
    monkeypatch.setattr(erpnext_customers, "read_only_database", database)

    result = erpnext_customers.read_recent_customers()

    assert result is records
    assert len(database.calls) == 1
    query, values = database.calls[0]
    normalized_query = " ".join(query.lower().split())
    assert "from `tabcustomer`" in normalized_query
    for field in (
        "name",
        "customer_name",
        "customer_group",
        "territory",
        "disabled",
    ):
        assert field in normalized_query
    assert "order by creation desc" in normalized_query
    assert not any(keyword in normalized_query for keyword in ("insert", "update", "delete"))
    assert values == {"limit": 10}


def test_read_recent_customers_respects_the_requested_limit(monkeypatch) -> None:
    database = FakeReadOnlyDatabase([])
    monkeypatch.setattr(erpnext_customers, "read_only_database", database)

    erpnext_customers.read_recent_customers(limit=4)

    assert len(database.calls) == 1
    assert database.calls[0][1] == {"limit": 4}
