from model.sqlalchemy.base import Base
from typing import Optional, List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


# follower_id is foreign key to user.id
class Following(Base):
    __tablename__ = "following"

    follower_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)

    follower: Mapped["User"] = relationship(
        "User", back_populates="following", foreign_keys=[follower_id]
    )
    followed: Mapped["User"] = relationship(
        "User", back_populates="followers", foreign_keys=[followed_id]
    )