import os
from sqlalchemy import create_engine, Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Create SQLAlchemy engine with CockroachDB dialect
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert postgresql:// to cockroachdb:// for CockroachDB compatibility
database_url = database_url.replace('postgresql://', 'cockroachdb://', 1).replace('postgres://', 'cockroachdb://', 1)

engine = create_engine(database_url, pool_pre_ping=True)

# Create base class for declarative models
Base = declarative_base()

# Define Todo model
class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    
    def to_dict(self):
        """Convert Todo instance to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Get a database session"""
    return SessionLocal()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print('Database initialized!')

if __name__ == '__main__':
    init_db()
