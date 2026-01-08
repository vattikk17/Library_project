from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple

from .interfaces import Task


ALLOWED_STATUSES = {"todo", "in_progress", "blocked", "done"}


@dataclass
class SimpleTask(Task):
    """
    Проста реалізація завдання для навчального проєкту.

    Поля:
    - task_id: унікальний ідентифікатор
    - title/description: назва та опис
    - _status: поточний статус
    - history: історія змін (timestamp, action, details)
    """
    task_id: int
    title: str = ""
    description: str = ""
    _status: str = "todo"
    history: List[Tuple[str, str, str]] = field(default_factory=list)

    def create(self, title: str, description: str = "") -> None:
        title = (title or "").strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        self.title = title
        self.description = (description or "").strip()
        self._log("create", f"title='{self.title}'")

    def edit(self, title: str | None = None, description: str | None = None) -> None:
        if title is not None:
            new_title = title.strip()
            if not new_title:
                raise ValueError("Task title cannot be empty.")
            self.title = new_title

        if description is not None:
            self.description = description.strip()

        self._log("edit", f"title='{self.title}'")

    def set_status(self, status: str) -> None:
        normalized = (status or "").strip().lower()
        if normalized not in ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Allowed: {sorted(ALLOWED_STATUSES)}"
            )

        old = self._status
        self._status = normalized
        self._log("status_change", f"{old} -> {self._status}")

    def get_status(self) -> str:
        return self._status

    def _log(self, action: str, details: str) -> None:
        ts = datetime.utcnow().isoformat(timespec="seconds")
        self.history.append((ts, action, details))

    def __repr__(self) -> str:
        return f"<SimpleTask id={self.task_id} title='{self.title}' status={self._status}>"
