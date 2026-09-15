"""ERPNext Customer access for the Build Factory intake exercise."""

from erpnext_database import read_only_database


def read_recent_customers(limit: int = 10) -> list[dict[str, object]]:
    """Return recently created ERPNext Customer records.
    """
    query = """
        SELECT name, customer_name, customer_group, territory, disabled
        FROM `tabCustomer`
        ORDER BY creation DESC
        LIMIT %(limit)s
    """
    return read_only_database.sql(query, {"limit": limit})
