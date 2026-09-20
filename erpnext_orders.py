"""ERPNext Sales Order access for the Build Factory pilot exercise."""

from erpnext_database import read_only_database


def read_recent_orders(limit: int = 10) -> list[dict[str, object]]:
    """Return recent ERPNext Sales Orders.

    Results are ordered newest-first by transaction date.
    """
    return read_only_database.sql(
        """
        SELECT
            name,
            customer,
            transaction_date,
            status,
            grand_total
        FROM `tabSales Order`
        ORDER BY transaction_date DESC
        LIMIT %(limit)s
        """,
        {"limit": limit},
    )
