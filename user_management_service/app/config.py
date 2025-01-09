import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/user_db")
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/user_db"

SECRET_KEY = os.getenv("SECRET_KEY", "bbd01a4b442b02a71985b200f7b5257cbdf145d5b8ff61916c0768cfc39f8281")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30