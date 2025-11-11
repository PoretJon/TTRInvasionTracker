from db_handler import FlippyDB
import os, dotenv

dotenv.load_dotenv()

# print(os.getenv("user"))
db_params = f"dbname={os.getenv("dbname")} user={os.getenv("user")} password={os.getenv("password")} host={os.getenv("host")} port={os.getenv("port")}"

flip = FlippyDB(db_params)

flip.reset_tables()

flip.register_server("1232123", "22332")
flip.register_user_to_server("some_id", "1232123")

flip.register_cog_for_user("some_id", "Backstabber")

print(flip.get_server_list())
print(flip.get_all_pings_for_server("1232123", "Backstabber"))

flip.register_server("1234567", "another_channel")
flip.register_user_to_server("some_id", "1234567")

print(flip.get_server_list())
print(flip.get_all_pings_for_server("1234567", "Backstabber"))
