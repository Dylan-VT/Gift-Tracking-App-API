#created 10/20 by Dylan Lawrence
#This document will hold all of the table schemas, making queries safer and easier

from typing import List
from sqlalchemy import Date, Table, Column, Integer, String, MetaData, ARRAY
from sqlalchemy.dialects.postgresql import array


metadata_obj = MetaData()
users = Table(
    "users",
    metadata_obj,
    Column("user_id", Integer, primary_key=True, nullable = True),
    Column("username", String),
    Column("display_name", String),
    Column("birthday", Date),
    Column("friends", ARRAY(Integer))
)