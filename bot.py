from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

updater = Updater(token='1308710409:AAFL1pYlnNqdN9FovzFcUHFyyePgVK1vShQ', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot and I fuck you в рот.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
