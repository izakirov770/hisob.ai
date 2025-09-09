from sqlalchemy import String, Integer, BigInteger, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base
import enum

class LangEnum(str, enum.Enum):
    uz = "uz"
    ru = "ru"
    en = "en"

class TxType(str, enum.Enum):
    income = "income"
    expense = "expense"

class DebtDir(str, enum.Enum):
    take = "take"   # olgan
    give = "give"   # bergen

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32))
    lang: Mapped[str] = mapped_column(String(2), default="uz")
    currency: Mapped[str] = mapped_column(String(8), default="UZS")
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all,delete-orphan")
    debts: Mapped[list["Debt"]] = relationship(back_populates="user", cascade="all,delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(Enum(TxType))
    amount: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    user: Mapped["User"] = relationship(back_populates="transactions")

class Debt(Base):
    __tablename__ = "debts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    direction: Mapped[str] = mapped_column(Enum(DebtDir))
    person: Mapped[str] = mapped_column(String(64))
    amount: Mapped[int] = mapped_column(Integer)
    due_date: Mapped["DateTime"] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="debts")
