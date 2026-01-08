from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass(frozen=True)
class ResourceAllocation:
    """
    Опис ресурсу, який виділяється на завдання.
    Наприклад: resource_name="Dev#1", units=6.0 (годин).
    """
    resource_name: str
    units: float


class Task(ABC):
    """
    Інтерфейс 'Завдання':
    - створення
    - редагування
    - відстеження/зміна стану
    """

    @abstractmethod
    def create(self, title: str, description: str = "") -> None:
        raise NotImplementedError

    @abstractmethod
    def edit(self, title: str | None = None, description: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_status(self, status: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> str:
        raise NotImplementedError


class Project(ABC):
    """
    Інтерфейс 'Проєкт':
    - керування списком завдань
    - додавання нових завдань
    - розподіл ресурсів
    """

    @abstractmethod
    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_tasks(self) -> Iterable[Task]:
        raise NotImplementedError

    @abstractmethod
    def allocate_resources(self, task: Task, allocations: list[ResourceAllocation]) -> None:
        raise NotImplementedError


class Notifier(Protocol):
    """
    Інтерфейс сповіщення:
    - надсилання повідомлень про події та зміни
    """

    def notify(self, event: str, message: str) -> None:
        ...
