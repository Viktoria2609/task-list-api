from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    is_complete: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : self.is_complete
        }
    
    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title = request_body["Name"],
            description = request_body["description"],
        )