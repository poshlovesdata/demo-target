"""Minimal read-only SQL boundary for the ERPNext pilot exercise."""

from collections.abc import Mapping
from typing import Protocol


class ReadOnlyDatabase(Protocol):
    """Read-only SQL operations available to the ERPNext integration."""

    def sql(
        self, query: str, values: Mapping[str, object]
    ) -> list[dict[str, object]]:
        """Execute a read query and return its records."""


class UnconfiguredReadOnlyDatabase:
    """Safe default used until the application supplies a real database."""

    def sql(
        self, query: str, values: Mapping[str, object]
    ) -> list[dict[str, object]]:
        raise RuntimeError("A read-only database has not been configured")


read_only_database: ReadOnlyDatabase = UnconfiguredReadOnlyDatabase()
