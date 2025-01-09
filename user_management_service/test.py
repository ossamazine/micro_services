from app.database.connection import engine

try:
    with engine.connect() as conn:
        print("Connected to the database successfully!")
except Exception as e:
    print("Database connection failed:", e)
