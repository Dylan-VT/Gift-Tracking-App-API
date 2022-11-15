"""
File to hold all of the functions for event requests
"""
from fastapi import HTTPException

from utils.metadata import events, users
from utils.sql_utils import make_simple_query
from models import event_models



def add_event(new_event: event_models.Event, engine):
    """
    Adds event to database
    """
    #first verify owner and user the event is for exist
    select = users.select().where(users.c.user_id == new_event.owner)
    owner = make_simple_query(select, engine).fetchone()
    if owner is None:
        print("Error: Could not find event owner")
        return 401

    #repeat for user
    select = users.select().where(users.c.user_id == new_event.event_for)
    owner = make_simple_query(select, engine).fetchone()
    if owner is None:
        print("Error: Could not find event user target")
        return 402

    #confirm event_name and event_date are not null
    if new_event.event_name is None or new_event.event_date is None:
        print("Error: Request not fully populated")
        return 403


    try:
        insert = events.insert().values(
            owner = new_event.owner,
            event_for = new_event.event_for,
            event_name = new_event.event_name,
            event_description = new_event.event_description,
            event_date = new_event.event_date
        )
        print(insert)
        make_simple_query(insert, engine)

    except Exception as exc:
        print(f'Error: {exc}')
        raise HTTPException(status_code=400, detail=f'Error making query: {exc}') from exc

    return 200



def get_events(users_list: str, engine):
    """
    Takes a list of users in comma seperated format.
    Gets a list of events relating to those users
    """
    #parse user list to ints
    try:
        user_id_list = [int(user) for user in users_list.split(',')]

    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=400, detail="Error parsing user IDs. Make sure all IDs are"
                            + " valid integers. Ex: /get_events/2,10,15") from exc

    #make query
    try:
        select = events.select().where(
            events.c.owner.in_(user_id_list)
        )

        results = make_simple_query(select, engine).fetchall()
        return results
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Error fetching users. "
                            + "Make sure database is up.") from exc
