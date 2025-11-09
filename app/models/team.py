from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Team(Base):
    """Baseball team model"""
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_sports_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    logo: Mapped[str] = mapped_column(String, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}', api_sports_id={self.api_sports_id})>"

