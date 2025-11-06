from db_handler import FlippyDB
import os, dotenv

dotenv.load_dotenv()

# print(os.getenv("user"))
db_params = f"dbname={os.getenv("dbname")} user={os.getenv("user")} password={os.getenv("password")} host={os.getenv("host")} port={os.getenv("port")}"

flip = FlippyDB(db_params)

flip.reset_tables()

flip.register_server("1232123", "22332")

print(flip.get_server_list())
