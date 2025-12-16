import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(os.getenv('DATABASE_URL'))

# Create base class for declarative models
Base = declarative_base()

# Define Todo model
class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
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
