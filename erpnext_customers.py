"""ERPNext Customer access for the Build Factory intake exercise."""

from erpnext_database import read_only_database


def read_recent_customers(limit: int = 10) -> list[dict[str, object]]:
    """Return recently created ERPNext Customer records.

    Results are ordered newest first and returned directly from the read-only
    database boundary.
    """
    return read_only_database.sql(
        """
        SELECT
            name,
            customer_name,
            customer_group,
            territory,
            disabled
        FROM `tabCustomer`
        ORDER BY creation DESC
        LIMIT %(limit)s
        """,
        {"limit": limit},
    )
