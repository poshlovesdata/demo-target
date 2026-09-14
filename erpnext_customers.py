"""ERPNext Customer access for the Build Factory intake exercise."""

from erpnext_database import read_only_database


def read_recent_customers(limit: int = 10) -> list[dict[str, object]]:
    """Return recently created ERPNext Customer records.

    This function is intentionally unfinished for the Build Factory exercise.
    """
    raise NotImplementedError("Implement recent ERPNext Customer retrieval")
