import asyncio
from datetime import timedelta, datetime

from telethon import TelegramClient, events
from sqlalchemy.orm import sessionmaker
from db_test.models import engine, ChatMessage, Base
import config

api_id = config.api_id
api_hash = config.api_hash
bot_token = config.bot_token

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


@client.on(events.NewMessage)
async def handler(event):
    if not session.query(ChatMessage).filter_by(message_id=event.message.id).first():
        new_message = ChatMessage(
            chat_id=event.chat_id,
            message_id=event.message.id,
            sender_id=event.message.sender_id,
            text=event.message.message,
            date=event.message.date
        )
        session.add(new_message)
        session.commit()


@client.on(events.NewMessage(pattern='/last_messages'))
async def handle_last_messages(event):
    chat_id = str(event.chat_id)
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    messages = session.query(ChatMessage).filter(
ChatMessage.chat_id == chat_id,
        ChatMessage.date >= yesterday
    ).order_by(ChatMessage.date).all()

    if messages:
        response = '\n'.join([f'{msg.date} - {msg.text}' for msg in messages])
    else:
        response = 'Нет сообщений за последний день.'

    await event.respond(response)


async def main():
    print("Bot is running...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())