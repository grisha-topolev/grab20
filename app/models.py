#app/models.py
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app import db


class Submission(db.Model):
    __tablename__: str = 'submissions'

    id: int = db.Column(db.Integer, primary_key=True)
    data: dict = db.Column(JSONB, nullable=False)
    created_at: datetime | None = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self) -> dict[str, object | None]:
        return {
            'id': self.id,
            'data': self.data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }