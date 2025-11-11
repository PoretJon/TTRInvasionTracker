import psycopg2

"""
* Flippy! db_handler.py
* Author: Jon Poret 2025
* Purpose: Handles all logic surrounding a PostgreSQL database for Flippy!.
"""


class FlippyDB:

    def __init__(self, db_connection_params):
        self.db_connection = db_connection_params
        self.psycopg_obj = psycopg2.connect(self.db_connection)

    """
    Resets the database.
    This should only be used for testing.
    """

    def reset_tables(self):
        with open("schema.sql", "r") as schema_file:
            schema_sql = schema_file.read()
        cursor = self.psycopg_obj.cursor()
        cursor.execute(schema_sql)
        self.psycopg_obj.commit()
        cursor.close()

    """
    Executes an SQL Query.
    
    Returns the result of a query if and only if 
    the sql query is meant to return something.
    Otherwise, this function returns null.

    TODO: Determine if this needs to two separate functions.
    """

    def run_query(self, query, params=None):
        cursor = self.psycopg_obj.cursor()
        cursor.execute(query, params)
        try:
            results = cursor.fetchall()
            cursor.close()
            return results
        except:
            pass
        cursor.close()

    """
    Initiates Flippy! working in a server
    registers the server and the correct channel in the db.
    """

    def register_server(self, guild_id: str, channel_id: str):
        sql_query = """
        INSERT INTO SERVER_SETTINGS (guild_id, channel_id) VALUES
        (%(guild_id)s, %(channel_id)s)
        ON CONFLICT (guild_id) DO UPDATE
        SET channel_id = %(channel_id)s
        """
        params = {"guild_id": guild_id, "channel_id": channel_id}
        self.run_query(sql_query, params)

    """
    Gets the users for a specific server that need to be pinged

    Not doing any special parsing of the returned list by psycopg, that is up to the user.
    """

    def get_all_pings_for_server(self, guild_id: str, cog_name: str):
        sql_query = """
        SELECT u.user_id FROM USER_SETTINGS as u
        INNER JOIN USER_COG_NOTIFS as cn on cn.user_id = u.user_id
        WHERE cn.cog_name = %(cog_name)s AND u.guild_id = %(guild_id)s
        """
        params = {"guild_id": guild_id, "cog_name": cog_name}
        res = self.run_query(sql_query, params)
        return res

    def register_user_to_server(self, user_id, guild_id):
        sql_query = """
        INSERT INTO USER_SETTINGS (user_id, guild_id) VALUES
        (%(user_id)s, %(guild_id)s)
        ON CONFLICT (user_id) DO UPDATE
        SET guild_id = %(guild_id)s
        """
        self.run_query(sql_query, params={"user_id": user_id, "guild_id": guild_id})

    def register_cog_for_user(self, user_id, cog_name):
        sql_query = """
            INSERT INTO USER_COG_NOTIFS (user_id, cog_name) VALUES
            (%(user_id)s, %(cog_name)s)
        """
        self.run_query(sql_query, params={"user_id": user_id, "cog_name": cog_name})

    def get_server_list(self):
        sql_query = """
            SELECT * FROM SERVER_SETTINGS
        """
        res = self.run_query(sql_query)
        return res
