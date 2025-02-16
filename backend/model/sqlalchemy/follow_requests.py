from model.sqlalchemy.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


# follower_id is foreign key to user.id
class FollowRequest(Base):
    __tablename__ = "follow_request"

    requester_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)
    requested_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), primary_key=True)
    
    requester: Mapped["User"] = relationship(
        "User", back_populates="requester", foreign_keys=[requester_id]
    )
    requested: Mapped["User"] = relationship(
        "User", back_populates="requested", foreign_keys=[requested_id]
    )