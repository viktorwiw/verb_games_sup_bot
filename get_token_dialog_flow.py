import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from environs import Env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


logger = logging.getLogger(__name__)


def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f'My first API key - {suffix}'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key

    client.create_key(request=request).result()


def main():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(name)s | %(levelname)s | %(asctime)s\n"
        "%(message)s | %(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler(Path(__file__).parent / 'create_api_key.log', maxBytes=300, backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')
    suffix = env.str('UNIQUE_SUFFIX')
    try:
        create_api_key(project_id,suffix)
        print('Successfully created an API key')
    except Exception as e:
        logger.exception(f'Ошибка при создании API-key:{e}')


if __name__ == '__main__':
    main()
