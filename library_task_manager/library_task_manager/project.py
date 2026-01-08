from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from .interfaces import Project, ResourceAllocation, Task


@dataclass
class SimpleProject(Project):
    """
    Проста реалізація 'Проєкт' для навчального проєкту.

    - Зберігає список завдань
    - Дозволяє додавати завдання
    - Дозволяє розподіляти ресурси по завданнях
    """
    name: str
    _tasks: List[Task] = field(default_factory=list)
    _allocations: Dict[int, List[ResourceAllocation]] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        if task is None:
            raise ValueError("Task cannot be None.")

        # Забороняємо дублікати за task_id (якщо він є)
        task_id = self._get_task_id(task)
        if any(self._get_task_id(t) == task_id for t in self._tasks):
            raise ValueError(f" with id={task_id} already exists in project.")

        self._tasks.append(task)

    def list_tasks(self) -> Iterable[Task]:
        return list(self._tasks)

    def allocate_resources(self, task: Task, allocations: list[ResourceAllocation]) -> None:
        if task is None:
            raise ValueError("Task cannot be None.")
        if allocations is None:
            raise ValueError("Allocations cannot be None.")

        task_id = self._get_task_id(task)

        # Перевіримо, що таке завдання реально в проєкті
        if not any(self._get_task_id(t) == task_id for t in self._tasks):
            raise ValueError(f" with id={task_id} is not in this project.")

        # Базова валідація ресурсів
        normalized: List[ResourceAllocation] = []
        for a in allocations:
            if not a.resource_name.strip():
                raise ValueError(".")
            if a.units <= 0:
                raise ValueError(".")
            normalized.append(a)

        self._allocations[task_id] = normalized

    def get_allocations(self, task: Task) -> list[ResourceAllocation]:
        """
        Додатковий метод (не з інтерфейсу), але корисний для демо/тестів.
        """
        task_id = self._get_task_id(task)
        return list(self._allocations.get(task_id, []))

    @staticmethod
    def _get_task_id(task: Task) -> int:
        """
        Для навчального проєкту очікуємо, що Task-реалізація має атрибут task_id:int.
        """
        task_id = getattr(task, "task_id", None)
        if not isinstance(task_id, int):
            raise TypeError("Task must have integer attribute 'task_id'.")
        return task_id
