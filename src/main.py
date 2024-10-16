"""Телеграм-бот для получения исторических справок."""

import os
from telethon import TelegramClient, events
import wikipedia


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    from dotenv import load_dotenv

    load_dotenv(dotenv_path)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Добро пожаловать в клуб любителей истории "У Санька"!')
    raise events.StopPropagation


@bot.on(events.NewMessage)
async def query(event):
    """Справка из Википедии."""
    wikipedia.set_lang("ru")
    summary = wikipedia.summary(event.text)
    await event.respond(summary)


def main():
    """Start the bot."""
    print("Starting the bot...")
    bot.run_until_disconnected()
    print("Bye!")


if __name__ == "__main__":
    main()
