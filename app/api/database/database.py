# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import Session
# from contextlib import contextmanager

# DATABASE_URL = "postgresql://Postgres_sql_owner:z31bWYweGVFd@ep-white-tree-a7pollpn-pooler.ap-southeast-2.aws.neon.tech/Postgres_sql?sslmode=require"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency for FastAPI

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://Postgres_sql_owner:z31bWYweGVFd@ep-white-tree-a7pollpn-pooler.ap-southeast-2.aws.neon.tech/Postgres_sql?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800  # Helps with stale connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

