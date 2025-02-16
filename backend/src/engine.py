from sqlalchemy import create_engine
import os

postgresql_url = os.getenv("DATABASE_URL")
if not postgresql_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# use this engine to connect to the database
postgresql_engine = create_engine(postgresql_url, echo=True)
