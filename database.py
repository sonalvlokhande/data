from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry



# Create the registry object
mapper_registry = registry()


# MySQL Database URL
#SQLALCHEMY_DATABASE_URL = "mysql://root:MahitNahi%4012@localhost/data_project"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MahitNahi%4012@localhost/larg_data"



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  #Base.metadata.create_all(bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# Utility function to dynamically add columns
def add_column_if_not_exists(table_name, column_name, column_type, session):
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]

    if column_name not in columns:
        session.execute(
            text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        )
        session.commit()

