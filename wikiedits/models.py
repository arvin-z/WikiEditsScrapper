from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
edit_tag = Table('edit_tag', Base.metadata,
    Column('edit_id', Integer, ForeignKey('wikiedit.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Edit(Base):
    __tablename__ = "wikiedit"

    id = Column(Integer, primary_key=True)
    ip_addr = Column('edit_ip_addr', Text())
    change = Column('edit_change', Text())
    new_words = Column('edit_new_words', Text())
    tags = relationship('Tag', secondary='edit_tag',
        lazy='dynamic', backref="wikiedit")  # M-to-M for quote and tag




class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    edits = relationship('Edit', secondary='edit_tag',
        lazy='dynamic', backref="tag")  # M-to-M for quote and tag
