"""ERPNext Sales Order access for the Build Factory pilot exercise."""

from erpnext_database import read_only_database


def read_recent_orders(limit: int = 10) -> list[dict[str, object]]:
    """Return recent ERPNext Sales Orders.

    This function is intentionally unfinished for the Build Factory exercise.
    """
    raise NotImplementedError("Implement recent ERPNext Sales Order retrieval")
