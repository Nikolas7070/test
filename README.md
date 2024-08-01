Here's the `README.md` file in English:

---

# Telegram Bot and Database Integration

## Description

This project includes a Telegram bot that uses the Telethon library to fetch messages and store them in a PostgreSQL database using SQLAlchemy. It also allows querying messages from the past day with the `/last_messages` command.

## Project Structure

### File 1: `main.py`

This file contains the main code for the bot. It performs the following tasks:
1. Connects to the Telegram API using Telethon.
2. Configures the database using SQLAlchemy.
3. Saves new messages to the database if they are not already present.
4. Responds to the `/last_messages` command with messages from the past day.

#### Key Functions:

- `handler(event)`: Handles new messages and saves them to the database.
- `handle_last_messages(event)`: Responds with a list of messages from the past day for the `/last_messages` command.
- `main()`: Runs the bot and keeps it active until disconnected.

### File 2: `models.py`

This file contains database model definitions using SQLAlchemy. It includes:

- Definition of the `chat_messages` table which stores message information.
- Database connection setup for PostgreSQL.

#### Key Functions:

- `ChatMessage`: Model for the message table in the database.
- `engine` and `Session`: Configuration for database connection and session creation.

## Requirements

- Python 3.12
- Libraries: `telethon`, `sqlalchemy`, `psycopg2`

Install all dependencies:

```sh
pip install telethon sqlalchemy psycopg2
```

## Configuration

Create a `config.py` file with your connection details:

```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'
DB_URL = 'postgresql://user:password@localhost/dbname'
```

## Running

To start the bot, run:

```sh
python main.py
```

## Running via Cron

If you want to run the script via `cron`, make sure you have the `telethon` module installed in your virtual environment and add the following cron job:

```sh
* * * * * /path/to/your/virtualenv/bin/python /path/to/your/main.py >> /path/to/your/cron.log 2>&1
```

Replace `/path/to/your/virtualenv` and `/path/to/your/main.py` with the appropriate paths.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This `README.md` file should help users understand how to use and run your project.
