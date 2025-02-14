import logging

from environs import Env
from telegram import Update, Bot
from telegram.ext import (Updater, CallbackContext, CommandHandler,
                          Filters, MessageHandler)
from telegram.error import NetworkError

from utils import detect_intent_texts


logger = logging.getLogger('tg_loger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id =chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def get_response(update: Update, context: CallbackContext) -> None:
    project_id = context.bot_data['project_id']
    session_id = update.effective_user.id
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
        logger.error(f'Ошибка на стороне API: {e}')


def main() -> None:
    logger = logging.getLogger('tg_loger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s\n"
        "%(message)s\n"
        "%(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')
    project_id = env.str('PROJECT_ID')
    chat_id = env.str('TG_CHAT_ID')

    updater = Updater(tg_token)
    dp = updater.dispatcher

    dp.bot_data["project_id"] = project_id

    tg_handler = TelegramLogsHandler(updater.bot, chat_id)
    tg_handler.setFormatter(formatter)
    logger.addHandler(tg_handler)

    dp.add_handler(CommandHandler("start", start))
    try:
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_response))
    except Exception as e:
        logger.error(e)

    try:
        logger.info("Бот запущен")
        updater.start_polling()
        updater.idle()
    except NetworkError as e:
        logger.error(f'Проблеммы с сетью: {e}')


if __name__ == '__main__':
    main()
