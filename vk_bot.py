import random
import logging

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import VkApiError
from telegram import Bot

from utils import detect_intent_texts


logger = logging.getLogger('vk_logger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot:Bot, chat_id):
        super().__init__()
        self.chat_id =chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_response(event, vk_api, project_id):
    session_id = event.user_id
    text = event.text
    language_code = 'ru-Ru'
    try:
        bot_response = detect_intent_texts(
            project_id,
            session_id,
            text,
            language_code
        )
        vk_api.messages.send(
            user_id=event.user_id,
            message=bot_response,
            random_id=random.randint(1,1000)
        )
    except Exception as e:
        logger.error(f'Ошибка на стороне API: {e}')


def main():
    logger = logging.getLogger('vk_logger')
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
    vk_token = env.str('VK_TOKEN')
    project_id = env.str('PROJECT_ID')
    chat_id = env.str('TG_CHAT_ID')

    bot = Bot(token=tg_token)

    tg_handler = TelegramLogsHandler(bot, chat_id)
    tg_handler.setFormatter(formatter)
    logger.addHandler(tg_handler)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('Бот VK запущен')
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                get_response(event, vk_api, project_id)
    except VkApiError as e:
        logger.error(f'Ошибка на стороне VK_API: {e}')


if __name__ == '__main__':
    main()
