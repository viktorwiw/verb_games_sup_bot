import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler
from telegram.error import NetworkError


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def start(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def get_response(update: Update, context: CallbackContext) -> None:
    project_id = context.bot_data['project_id']
    session_id = update.effective_user.id
    text = update.message.text
    language_code = 'ru-Ru'
    try:
        bot_response = detect_intent_texts(project_id, session_id, text, language_code)
        update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f'Ошибка на стороне API: {e}')


def detect_intent_texts(project_id, session_id, text, language_code) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
        )
    return response.query_result.fulfillment_text


def main() -> None:
    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')
    project_id = env.str('PROJECT_ID')

    bot = Updater(tg_token)
    dp = bot.dispatcher

    dp.bot_data["project_id"] = project_id

    logger.info("Bot started")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_response))

    try:
        bot.start_polling()
        bot.idle()
    except NetworkError as e:
        logger.error(f'Проблеммы с сетью: {e}')


if __name__ == '__main__':
    main()
