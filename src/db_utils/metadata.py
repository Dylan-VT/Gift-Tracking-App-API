'''
created 10/20 by Dylan Lawrence
This document will hold all of the table schemas, making queries safer and easier
'''

from sqlalchemy import Date, Table, Column, Integer, String, MetaData, ARRAY


metadata_obj = MetaData()
users = Table(
    "users",
    metadata_obj,
    Column("user_id", Integer, primary_key=True, nullable = True),
    Column("username", String),
    Column("display_name", String),
    Column("birthday", Date),
    Column("friends", ARRAY(Integer()))
)

events = Table(
    "events",
    metadata_obj,
    Column('owner', Integer, primary_key=True),
    Column('event_for', Integer),
    Column('event_name', String),
    Column('event_description', String, nullable = True),
    Column('event_date', Date)
)
