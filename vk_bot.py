import random
import logging

from google.cloud import dialogflow
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def detect_intent_texts(project_id, session_id, text, language_code) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)


    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
        )
    if response.query_result.intent.is_fallback:
        return

    return response.query_result.fulfillment_text


def get_response(event, vk_api, project_id):
    session_id = event.user_id
    text = event.text
    language_code = 'ru-Ru'
    try:
        bot_response = detect_intent_texts(project_id, session_id, text, language_code)
        vk_api.messages.send(
            user_id=event.user_id,
            message=bot_response,
            random_id=random.randint(1,1000)
        )
    except Exception as e:
        logger.error(f'Ошибка на стороне API: {e}')


def main():
    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    project_id = env.str('PROJECT_ID')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_response(event, vk_api, project_id)


if __name__ == '__main__':
    main()
