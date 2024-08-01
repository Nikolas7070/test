from sqlalchemy import Column, BigInteger, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

Base = declarative_base()


class ChatMessage(Base):
    tablename = 'chat_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False, unique=True)
    sender_id = Column(BigInteger, nullable=False)
    text = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)


DATABASE_URL = config.DB_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
