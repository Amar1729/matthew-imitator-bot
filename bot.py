#! /usr/bin/env python3

"""
about - short info for this bot
"""

import datetime
import logging
import os
from typing import Optional

# third-party
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

# local
from settings import TOKEN, TZ, GROUP_CHAT_ID


MSG_FILE = "message.log"

WORDLE_START = 225
WORDLE_START_DATE = datetime.date(year=2022, month=1, day=30)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def about(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join([
            "I replicate a friend of my creator's in one of his primary chats.",
            "Check out my page!",
            "",
        ])
    )


def get_recent_message() -> Optional[int]:
    if os.path.exists(MSG_FILE):
        with open(MSG_FILE, "r") as f:
            return int(f.read().strip())

    return None


def save_message_id(message_id: int):
    with open(MSG_FILE, "w") as f:
        f.write(str(message_id))


def wordle(context: CallbackContext):
    td = datetime.datetime.now().date() - WORDLE_START_DATE
    weekday = datetime.datetime.now().strftime("%A")

    current = td.days + WORDLE_START

    msg = f"{weekday} wordle: {current}"

    sent_message = context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=msg,
    )

    if recent_msg := get_recent_message():
        context.bot.unpin_chat_message(
            chat_id=GROUP_CHAT_ID,
            message_id=recent_msg,
        )

    sent_message.pin()
    save_message_id(sent_message.message_id)


if __name__ == "__main__":
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    jobq = updater.job_queue
    jobq.run_daily(wordle, time=datetime.time(hour=0, tzinfo=TZ))

    dispatcher.add_handler(CommandHandler("about", about))

    updater.start_polling()
    updater.idle()
