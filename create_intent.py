import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from environs import Env
from google.api_core.exceptions import InvalidArgument, GoogleAPIError
from google.cloud import dialogflow


logger = logging.getLogger(__name__)


def get_questions():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts
):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.info("Intent created: {}".format(response))


def main():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
            "%(name)s | %(levelname)s | %(asctime)s\n"
        "%(message)s | %(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler(Path(__file__).parent / 'create_intent.log', maxBytes=1000, backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    env = Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")

    for display_name, intent in get_questions().items():
        training_phrases_parts = intent['questions']
        message_texts = [intent['answer']]
        try:
            create_intent(
                project_id,
                display_name,
                training_phrases_parts,
                message_texts
            )
        except InvalidArgument as e:
            logger.error(f'Интент уже существует: {e}')
        except GoogleAPIError as e:
            logger.error(f'Ошибка GoogleAPI: {e}')


if __name__ == '__main__':
    main()
