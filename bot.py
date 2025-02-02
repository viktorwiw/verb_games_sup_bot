import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
    logger.info(update)


def main() -> None:
    env = Env()
    env.read_env()

    tg_token = env.str("TELEGRAM_TOKEN")

    bot = Updater(tg_token)
    dp = bot.dispatcher

    logger.info("Bot started")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
