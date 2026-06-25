from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create_engine connects to your Neon database
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    # This creates the tables in Neon if they don't exist yet
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session