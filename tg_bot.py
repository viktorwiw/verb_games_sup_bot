import logging
from logging.handlers import RotatingFileHandler

from environs import Env
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (Updater, CallbackContext, CommandHandler,
                          Filters, MessageHandler)

from utils import detect_intent_texts


logger = logging.getLogger('tg_bot')


def start(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def get_response(update: Update, context: CallbackContext) -> None:
    project_id = context.bot_data['project_id']
    session_id = f'tg-{update.effective_user.id}'
    text = update.message.text
    language_code = 'ru-Ru'
    try:
        bot_response = detect_intent_texts(
            project_id,
            session_id,
            text,
            language_code
        )
        if bot_response:
            update.message.reply_text(bot_response)
        else:
            update.message.reply_text('Вопрос непонятен, дождитесь оператора')
    except Exception as e:
        logger.exception(f'Ошибка на стороне API: {e}')


def main() -> None:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(name)s | %(levelname)s | %(asctime)s\n"
        "%(message)s | %(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler('tg_bot.log', maxBytes=10000, backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')
    project_id = env.str('PROJECT_ID')

    updater = Updater(tg_token)
    dp = updater.dispatcher

    dp.bot_data["project_id"] = project_id

    try:
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_response))
    except Exception as e:
        logger.error(e)

    try:
        logger.info("Бот запущен")
        updater.start_polling()
        updater.idle()
    except NetworkError as e:
        logger.error(f'Проблемы мы с сетью: {e}')


if __name__ == '__main__':
    main()
