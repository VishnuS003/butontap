from typing import Optional
from sqlalchemy import BigInteger, Integer, String, CheckConstraint, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    coins:    Mapped[int] = mapped_column(Integer, default=0)
    diamonds: Mapped[int] = mapped_column(Integer, default=0)
    xp:       Mapped[int] = mapped_column(Integer, default=0)
    weekly_taps: Mapped[int] = mapped_column(Integer, default=0)
    week_anchor: Mapped[Optional[str]] = mapped_column(String(10), index=True)

    __table_args__ = (
        CheckConstraint("coins >= 0"),
        CheckConstraint("diamonds >= 0"),
        CheckConstraint("xp >= 0"),
        Index("ix_players_tgid", "telegram_user_id"),
    )
