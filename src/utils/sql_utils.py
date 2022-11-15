def make_simple_query(sql_statement, _e):
    """
    simple function that takes a sql statement and engine and returns the result of the query
    """
    #open connection
    with _e.connect() as conn:
        #make query
        result = conn.execute(sql_statement)
        return result