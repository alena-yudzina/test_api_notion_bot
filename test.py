import json
import os

from api_functions import readDatabase, updatePage
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from loguru import logger


api_token = os.getenv('SECRET_NOTION_TOKEN')
bot_token = os.getenv('BOT_TOKEN_TEST')

databaseId = 'f7cbfc43e5dc4b449cf4df163ffd9e9c'

pageId = '0b235e51-82c6-45a5-905a-4818877049f9'

headers = {
    "Authorization": "Bearer " + api_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

logger.add('debug.log', encoding="utf8", format='TIME: {time} LEVEL: {level} MESSAGE: {message}', rotation='10 MB', compression='zip')

def test():
    with open('./update.json') as f:
        updateData = json.load(f)

    print(updatePage(pageId, headers, updateData))

    data = readDatabase(databaseId, headers)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Отправляйте любые проблемы, а сенсей на ближайшем созвоне поможет вам решить их!")


def initTelegram():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # стандартные обработчики бота
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    #echo_handler = MessageHandler(Filters.text, echo)
    #dispatcher.add_handler(echo_handler)
    logger.info('Bot Polling Started')
    updater.start_polling()


if __name__ == "__main__":
    initTelegram()
