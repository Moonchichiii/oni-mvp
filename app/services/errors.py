from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepoError(Exception):
    message: str


@dataclass(frozen=True)
class DuplicateServiceName(RepoError):
    pass


@dataclass(frozen=True)
class RepoUnavailable(RepoError):
    pass
