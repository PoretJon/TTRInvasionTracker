from db_handler import FlippyDB
import os, dotenv

dotenv.load_dotenv()

# print(os.getenv("user"))
db_params = f"dbname={os.getenv("dbname")} user={os.getenv("user")} password={os.getenv("password")} host={os.getenv("host")} port={os.getenv("port")}"

flip = FlippyDB(db_params)

# flip.reset_tables()
# print("here?")

# flip.register_server("1232123", "22332")
# flip.register_user_to_server("some_id", "1232123")
# print("1")
# x = flip.register_cog_for_user("some_id", "Backstabber")
# print(x)

# print(flip.get_server_list())
# print(flip.get_all_pings_for_server("1232123", "Backstabber"))

# flip.register_server("1234567", "another_channel")
# flip.register_user_to_server("some_id", "1234567")

# print(flip.get_server_list())
# print(flip.get_all_pings_for_server("1234567", "Backstabber"))

# user_list = [id[0] for id in flip.get_all_pings_for_server("1234567", "Backstabber")]
# print(user_list)

user_list = flip.get_all_pings_for_server("1410043343047491646", "Back Stabber")
print(user_list)
