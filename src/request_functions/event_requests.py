"""
File to hold all of the functions for event requests
"""
from fastapi import HTTPException
import sqlalchemy as db
from db_utils.metadata import events, users, ideas
from db_utils.sql_utils import make_simple_query
from class_models import event_models



def add_event(new_event: event_models.Event, engine):
    """
    Adds event to database
    """

    #verify user exists
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
        
        select = db.select(
                [events, users.c.username]
                ).where(
                    events.c.event_for.in_(user_id_list)
                ).where(
                    events.c.event_for == users.c.user_id
                )

        results = make_simple_query(select, engine).fetchall()
        
        print(results)
        return results
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=400, detail="Error fetching users. "
                            + "Make sure database is up.") from exc


def add_idea(user_id: int, event_for: int, gift_name: str, engine):
    """
    Adds an idea to an event
    """
    #verify user exists
    select = users.select().where(users.c.user_id == user_id)
    owner = make_simple_query(select, engine).fetchone()
    if owner is None:
        print("Error: Could not find event user target")
        return 402

    select = users.select().where(users.c.user_id == event_for)
    other_user = make_simple_query(select, engine).fetchone()
    if other_user is None:
        print("Error: Could not find event user target")
        return 402

    #confirm gift_name is not null
    if gift_name is None:
        print("Error: Request not fully populated")
        return 404

    #select relevant idea row
    select_idea = ideas.select().where(ideas.c.user == user_id).where(ideas.c.event_for == event_for)
    idea_row = make_simple_query(select_idea, engine).fetchone()
    #if none create new column
    if idea_row is None:
        insert = ideas.insert().values(
            user = user_id,
            event_for = event_for,
            ideas = [gift_name]
        )
        new_ideas = make_simple_query(insert, engine)
        print(new_ideas)

    #else get row, and append to list, then update
    else:
        select = ideas.select().where(ideas.c.user == user_id).where(ideas.c.event_for == event_for)
        idea_row = make_simple_query(select, engine).fetchone()
        new_ideas = idea_row.ideas + [gift_name]
        #update
        update = ideas.update().where(ideas.c.user == user_id).where(ideas.c.event_for == event_for).values(ideas = new_ideas)
        try:
            make_simple_query(update, engine)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Error updating ideas.") from exc


    return 200

def get_idea(user: int, event_for: int, engine):
    """
    Gets an idea from an event
    """
    select = ideas.select().where(ideas.c.user == user).where(ideas.c.event_for == event_for)
    try:
        idea_row = make_simple_query(select, engine).fetchone()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Error fetching ideas.") from exc
    
    if idea_row is None:
        return [{"ideas": []}]
    return [{"ideas": idea_row.ideas}]