"""
This file will contain the functions used in endpoints relating to users
Created 11/15 by Dylan Lawrence
"""

from class_models import user_models
from db_utils.sql_utils import make_simple_query
from db_utils.metadata import users

def add_friend(new_friend_info: user_models.AddFriend, engine):
    '''
    query to create a new friend, takes the username of the original friend
    and the new friend to add
    '''
    #users cannot add themselves as friends
    if new_friend_info.username == new_friend_info.new_friend:
        return 501

    #first verify friend is exists
    select = users.select().where(
                            users.c.username == new_friend_info.new_friend)

    new_friend_result = make_simple_query(select, engine).fetchone()

    #return 201 if no friend
    if new_friend_result is None:
        print("Couldn't find new friend")
        return 502

    #get original users friends
    select = users.select().where(
                            users.c.username == new_friend_info.username
    )

    original_user = make_simple_query(select, engine).fetchone()

    #if no friends found or friend in list return a 5xx

    if original_user is None:
        return 503

    original_user_friends = original_user.friends  # type: ignore
    #instantiate list of friends if empty
    if original_user_friends is None:
        original_user_friends = []

    if new_friend_info.new_friend in original_user_friends:
        return 504

    #update original users friends
    original_user_friends.append(new_friend_result.user_id)  # type: ignore
    print(original_user_friends)

    #now update in db

    update = users.update().where(
        users.c.username == new_friend_info.username
    ).values(
        {"friends": original_user_friends}
    )


    make_simple_query(update, engine)

    return 200