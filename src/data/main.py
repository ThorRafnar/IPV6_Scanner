from enum import unique
from numpy import integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Table, ForeignKey, create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
import os


meta = MetaData()

DATABASE_NAME = "scan"


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
"""

"""
connection_string = 'sqlite:///'+os.path.join(BASE_DIR, f'{DATABASE_NAME}.sqlite3')
engine = create_engine(connection_string, echo=True)
Base = declarative_base()

session=sessionmaker()(bind=engine)

association_table = Table(
    'assosiation',
    Base.metadata,
    Column('address_id', ForeignKey('addresses.id')),
    Column('port_id', ForeignKey('ports.port'))
)

class Address(Base):
    __tablename__ = 'addresses'
    id=Column(Integer(), primary_key=True)
    address=Column(String(45), nullable=False, unique=True)
    ports=relationship(
        'Port',
        secondary=association_table,
        back_populates='addresses'
    )

class Port(Base):
    __tablename__ = 'ports'
    port=Column(Integer(), primary_key=True, unique=True)
    addresses=relationship(
        'Address',
        secondary=association_table,
        back_populates='ports'
    )



meta.create_all(engine)