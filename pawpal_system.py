"""Core domain skeleton for PawPal+ scheduling logic.

This module defines the main classes and method signatures used by the app.
Behavior is intentionally left as placeholders for incremental implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class CareTask:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str  # e.g., "low", "medium", "high"
    recurrence: str = "none"  # e.g., "none", "daily", "weekly"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def is_due_today(self) -> bool:
        """Return whether the task should run today.

        TODO: Add recurrence/date logic.
        """
        return True


@dataclass
class Pet:
    """Represents a pet and its care tasks."""

    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> bool:
        """Remove the first task matching title.

        Returns True if removed, False otherwise.
        """
        for index, task in enumerate(self.tasks):
            if task.title == task_title:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self) -> List[CareTask]:
        """Return this pet's current tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """Represents a pet owner and planning constraints."""

    name: str
    available_minutes_per_day: int
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def set_availability(self, minutes: int) -> None:
        """Update daily available time in minutes."""
        self.available_minutes_per_day = minutes

    def set_preferences(self, preferences: str) -> None:
        """Update owner preferences text."""
        self.preferences = preferences


class Scheduler:
    """Builds an ordered daily task plan using owner constraints."""

    def generate_daily_plan(self, owner: Owner) -> List[CareTask]:
        """Generate today's plan across all owner pets.

        TODO: Add real scheduling behavior.
        """
        all_tasks: List[CareTask] = []
        for pet in owner.pets:
            all_tasks.extend([task for task in pet.tasks if task.is_due_today()])

        sorted_tasks = self.sort_tasks(all_tasks)
        return self.filter_by_available_time(sorted_tasks, owner.available_minutes_per_day)

    def sort_tasks(self, tasks: List[CareTask]) -> List[CareTask]:
        """Return tasks sorted by priority and duration.

        TODO: Confirm/adjust sorting rules.
        """
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda task: (priority_rank.get(task.priority, 3), task.duration_minutes))

    def filter_by_available_time(self, tasks: List[CareTask], minutes: int) -> List[CareTask]:
        """Keep tasks that fit in the time budget."""
        plan: List[CareTask] = []
        used = 0
        for task in tasks:
            if used + task.duration_minutes <= minutes:
                plan.append(task)
                used += task.duration_minutes
        return plan

    def explain_plan(self, plan: List[CareTask]) -> str:
        """Return a short human-readable explanation of ordering."""
        if not plan:
            return "No tasks fit within the available time today."
        titles = ", ".join(task.title for task in plan)
        return f"Planned tasks were prioritized by importance and time fit: {titles}."
