from environs import Env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")

    return response


def main():
    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')
    suffix = env.str('UNIQUE_SUFFIX')
    create_api_key(project_id,suffix)


if __name__ == '__main__':
    main()
