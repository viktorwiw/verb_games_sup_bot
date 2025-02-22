import random
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import VkApiError

from utils import detect_intent_texts


logger = logging.getLogger('vk_bot')


def get_response(event, vk_api, project_id):
    session_id = f'vk-{event.user_id}'
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
        logger.exception(f'Ошибка на стороне API: {e}')


def main():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(name)s | %(levelname)s | %(asctime)s\n"
        "%(message)s | %(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler(Path(__file__).parent / 'vk_bot.log', maxBytes=10000, backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    project_id = env.str('PROJECT_ID')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('Бот VK запущен')

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                get_response(event, vk_api, project_id)
    except VkApiError as e:
        logger.exception(f'Ошибка на стороне VK_API: {e}')


if __name__ == '__main__':
    main()
