# backend/db.py

from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Define your model classes
class MyModel(Base):
    __tablename__ = 'my_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create the engine and tables
engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def print_table_creation_statements():
    metadata = MetaData()
    # Assuming you want to reflect existing tables or do something with metadata
    metadata.reflect(bind=engine)
    for table in (Base.metadata.sorted_tables):
        print(str(table), 'is created!!!')


# Call the function to print table creation statements
print_table_creation_statements()
