import os
from pathlib import Path
from datetime import datetime,timezone
from sqlalchemy import create_engine,Column,Integer,String,DateTime,Text
from sqlalchemy.orm import DeclarativeBase,sessionmaker
ROOT=Path(__file__).resolve().parents[2]
DATABASE_URL=os.getenv('DATABASE_URL',f'sqlite:///{ROOT / "streamiq.db"}')
engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine)
class Base(DeclarativeBase):pass
class SessionRecord(Base):
    __tablename__='simulation_sessions'
    id=Column(Integer,primary_key=True)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc))
    profile=Column(String(40),nullable=False)
    strategy=Column(String(20),nullable=False)
    seed=Column(Integer,nullable=False)
    summary=Column(Text,nullable=False)
    timeline=Column(Text,nullable=False)
Base.metadata.create_all(bind=engine)
