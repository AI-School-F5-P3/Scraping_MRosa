from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Birthdate(Base):
    __tablename__ = 'birthdate'
    id = Column(Integer, primary_key=True)
    birthdate = Column(Date, nullable=False)

class Birthplace(Base):
    __tablename__ = 'birthplace'
    id = Column(Integer, primary_key=True)
    birthplace = Column(String(255), nullable=False)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birthdate_id = Column(Integer, ForeignKey('birthdate.id'))
    birthplace_id = Column(Integer, ForeignKey('birthplace.id'))
    description = Column(Text)
    birthdate = relationship('Birthdate')
    birthplace = relationship('Birthplace')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), unique=True)

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')

class QuoteTag(Base):
    __tablename__ = 'quote_tags'
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quotes.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
