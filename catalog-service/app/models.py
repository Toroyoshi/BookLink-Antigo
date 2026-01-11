from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.db import Base

class Work(Base):
    __tablename__ = "works"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300), index=True)
    isbn: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subjects: Mapped[str | None] = mapped_column(String(500), nullable=True)  # comma-separated (simples)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    copies: Mapped[list["Copy"]] = relationship(back_populates="work", cascade="all,delete-orphan")

class Copy(Base):
    __tablename__ = "copies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_id: Mapped[int] = mapped_column(ForeignKey("works.id"), index=True)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="AVAILABLE", index=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    work: Mapped["Work"] = relationship(back_populates="copies")
