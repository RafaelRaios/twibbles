from sqlalchemy import String, Boolean
from sqlalchemy import ForeignKey
from model.sqlalchemy.base import Base

from typing import Optional, List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Especificando explicitamente foreign_keys para evitar ambiguidade
    following: Mapped[List["Following"]] = relationship(
        back_populates="follower",
        cascade="all, delete-orphan",
        foreign_keys="Following.follower_id"
    )
    
    followers: Mapped[List["Following"]] = relationship(
        back_populates="followed",
        cascade="all, delete-orphan",
        foreign_keys="Following.followed_id"
    )

    requester: Mapped[List["FollowRequest"]] = relationship(
        back_populates="requester",
        cascade="all, delete-orphan",
        foreign_keys="FollowRequest.requester_id"
    )
    
    requested: Mapped[List["FollowRequest"]] = relationship(
        back_populates="requested",
        cascade="all, delete-orphan",
        foreign_keys="FollowRequest.requested_id"
    )