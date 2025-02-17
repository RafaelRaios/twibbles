from sqlalchemy import String, DateTime
from sqlalchemy import ForeignKey
from model.sqlalchemy.base import Base

from typing import Optional, List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime as dt

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    date_time: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow, nullable=False)