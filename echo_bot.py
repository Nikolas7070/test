import asyncio
import sqlalchemy
from telethon import events, TelegramClient
from sqlalchemy import Column, Integer, String, create_engine, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

api_id = 20310652
api_hash = '930dbf84a62698e85b9ac1bf98fb539d'
bot_token = '7068689831:AAGA62cfx01K3J1_Y9cRCSHLeFVXGAWy2JI'

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

# Создаем клиента
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    message_text = event.message.message
    sender_id = event.sender_id

    # Сохраняем сообщение в базу данных
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

    if event.is_private:
        print('WORK')

    await event.reply(message_text)


@client.on(events.NewMessage(pattern='/last10'))
async def last10_handler(event):
    # Получаем последние 10 сообщений из базы данных
    last_10_messages = db_session.query(Message).order_by(desc(Message.timestamp)).limit(10).all()

    response = "Последние 10 сообщений:\n"
    for msg in last_10_messages:
        response += (f"{msg.timestamp} - {msg.first_name} {msg.last_name} (@{msg.username}): "
                     f"{msg.message_text}\n")

    print(response)


async def periodic_task():
    while True:
        print("Task running every 10 seconds")
        # Здесь вы можете добавить код для выполнения задачи
        await asyncio.sleep(10)


async def main():
    await client.start()
    await asyncio.gather(client.run_until_disconnected(), periodic_task())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
