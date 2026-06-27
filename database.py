from sqlmodel import SQLModel, create_engine, Session, select
from models import User
from auth import get_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    # SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = session.exec(select(User)).first()
        if not user:
            admin = User(
                username="admin@extractiq.com",
                hashed_password=get_password_hash("123")
            )
            session.add(admin)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session