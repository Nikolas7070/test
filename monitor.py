import asyncio
from asyncio import events
import sqlalchemy
from telethon import TelegramClient
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

api_id = 20310652
api_hash = '930dbf84a62698e85b9ac1bf98fb539d'

# Настройка базы данных
DATABASE_URL = 'postgresql://postgres:49952004@localhost:5432/test_siroshtanov'

Base = sqlalchemy.orm.declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    phone_number = Column(String)
    message_text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

client = TelegramClient('monitor', api_id, api_hash)


async def main():
    await client.start()

    @client.on(events.NewMessage)
    async def handler(event):
        sender = await event.get_sender()
        message_text = event.message.message
        sender_id = event.sender_id

        new_message = Message(
            sender_id=sender_id,
            first_name=sender.first_name,
            last_name=sender.last_name,
            username=sender.username,
            phone_number=sender.phone if sender.phone else None,
            message_text=message_text
        )
        db_session.add(new_message)
        db_session.commit()

    await client.run_until_disconnected()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
