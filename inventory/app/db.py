from sqlmodel import Session,create_engine,SQLModel, Field
from app import settings
from typing import Optional


class Inventory(SQLModel,table=True):
    id : int|None = Field(default=None, primary_key=True)
    product_id : int
    stock : Optional[int] =None

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)



engine = create_engine(
   connection_string, pool_recycle=300,
   echo=True
)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

