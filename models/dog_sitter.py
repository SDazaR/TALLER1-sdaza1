from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import db
from typing import List
from models.dog import Dog

class DogSitter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    dogs: Mapped[List["Dog"]] = relationship("Dog", backref="dog_sitter")