import json
import os
import requests
from dotenv import load_dotenv

from api_functions import readDatabase, createPage
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from loguru import logger


load_dotenv()

api_token = os.getenv('SECRET_NOTION_TOKEN')
bot_token = os.getenv('BOT_TOKEN_TEST')

problemsDatabaseId = os.getenv('PROBLEMS_DATABASE_ID')

pageId = ('PAGE_ID')

teachers_db = os.getenv('TEACHERS_DATABASE_ID')

headers = {
    "Authorization": "Bearer " + api_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

logger.add('debug.log', encoding="utf8",
           format='TIME: {time} LEVEL: {level} MESSAGE: {message}', rotation='10 MB', compression='zip')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Отправляйте любые проблемы, а сенсей на ближайшем созвоне поможет вам решить их!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Проблема отправляется. Это займёт некоторе время, но уже можно отправлять ещё')
    username = update.message.from_user.username
    message = update.message.text
    logger.info(f'padavan @{username} sent problem: {message}')
    try:
        createPage(problemsDatabaseId, headers, username, message)
        logger.info(f'problem sent to Notion: {message}')
        text = f'Проблема "{message[:10]}..." отправлена. Будьте уверены, сенсей вам с ней поможет :)'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logger.exception(e)
        logger.error(f'У бота что-то поломалось. Отправлял @{username} проблему "{message}"')
        text = 'Что-то пошло не так. Попробуйте повторить отправку через какое-то время, ' \
               'а пока сообщите об этом сенсею!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def initTelegram():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # стандартные обработчики бота
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    logger.info('Bot Polling Started')
    updater.start_polling()


if __name__ == "__main__":
    initTelegram()
    readUrl = f"https://api.notion.com/v1/databases/{teachers_db}/query"

    res = requests.request("POST", readUrl, headers=headers)

    with open('teacher.json', 'w') as f:
        json.dump(res.json(), f, ensure_ascii=False, indent=2)
