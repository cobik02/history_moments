"""Телеграм-бот для получения исторических справок."""

import os
from telethon import TelegramClient, events
import wikipedia
import re


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


ACTIONS = r"произош(ел|л[аио])|случил([аио]сь|ся)|был(а)?|начал([аио]сь|ся)|закончил([аио]сь|ся)"
QUERY_WHEN = r"Когда\s(?P<action>{})\s(?P<subject>[^?]+)\?".format(ACTIONS)
QUERY_PAT = re.compile(QUERY_WHEN)
DATE_PAT = re.compile(
    r"(?P<day>\d+(-\d+)?)\s(?P<month>января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s(?P<year>\d+) год",
    re.MULTILINE,
)


@bot.on(events.NewMessage(pattern=QUERY_WHEN))
async def query_when(event):
    """Запрос описания события.."""
    wikipedia.set_lang("ru")
    m = QUERY_PAT.match(event.text)
    action = m.group("action")
    subject = m.group("subject")
    summary = wikipedia.summary(subject)

    dates = []

    for m in DATE_PAT.finditer(summary):
        dates.append(f"{m.group('day')} {m.group('month')} {m.group('year')}")

    dates = ", ".join(dates)

    await event.respond(subject + "\n" + action + "\n" + summary + "\n" + dates)


def main():
    """Start the bot."""
    print("Starting the bot...")
    bot.run_until_disconnected()
    print("Bye!")


if __name__ == "__main__":
    main()
