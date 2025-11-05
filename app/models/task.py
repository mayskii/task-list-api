from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    @classmethod
    def from_dict(cls, task_data):

        goal_id = task_data.get("goal_id")

        new_task = cls(
            title = task_data["title"],
            description = task_data["description"],
            goal_id = goal_id,
            completed_at = task_data.get("completed_at")
        )
        return new_task
    
    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict
