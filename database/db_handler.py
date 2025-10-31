import psycopg2
from Information import CogInformation


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
        """
        params = {"guild_id": guild_id, "channel_id": channel_id}
        self.run_query(sql_query, params)

    """
    Gets the users for a specific server that need to be pinged
    """

    def get_all_pings_for_server(self, guild_id: str, cog_name: str):
        sql_query = """
        SELECT user_id FROM USER_SETTINGS
        WHERE cog_name = %(cog_name)s AND guild_id = %(guild_id)s
        """
        params = {"guild_id": guild_id, "cog_name": cog_name}
        res = self.run_query(sql_query, params)
