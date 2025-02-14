# verb_games_sup_bot

Чат - бот помощник для ответов на типичные вопросы. Бот работает как в Телеграмме так и в
социальной сети [VK](https://vk.com/)


## Как установить

Создайте в корне проекта, файл `.env` Пропишите в нем:

```
TG_TOKEN=ТОКЕН ВАШЕГО БОТА TELEGRAM
VK_TOKEN=ТОКЕН ВАШЕЙ ГРУППЫ В VK
PROJECT_ID=ID ПРОЕКТА В GOOGLE_CLOUD
UNIQUE_SUFFIX=ЛЮБОЕ УНИКАЛЬНОЕ ЗНАЧЕНИЕ
GOOGLE_APPLICATION_CREDENTIALS=ПУТЬ ДО CREDENRIALS.JSON
```
где:

`TG_TOKEN` - получить при создании телеграм бота в боте [BotFather](https://t.me/BotFather)
`VK_TOKEN` - Создайте сообщество в ВК, токен можно получить в настройках сообщества в разделе `Работа с API - Ключи доступа`
`PROJECT_ID` - ID проекта в Google Cloud
СКРИН
`GOOGLE_APPLICATION_CREDENTIALS` - Путь до credentials.json полученный при запуске и инициализации GoogleCLI

Для изоляции проекта рекомендуется развернуть виртуальное окружение:

для Linux и MacOS
```bash
python3 -m venv env
source env/bin/activate
```

для Windows
```bash
python -m venv env
venv\Scripts\activate.bat
```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```


## Тренировка DialogFlow

Для работы ботов, необходимо обучить DialogFlow на работу с вашими клиентами.

### Создайте проект в DialogFlow

[Как создать проект в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup)

`*СКРИН*`

Нам должны выдать такой идентификатор 
```
НАЗВАНИЕ ВАШЕГО ПРОЕКТА-211973
```

### Создайте агента и натренируйте его

Агент - это бот, который будет отвечать на вопросы пользователей и будем использовать его в своих ботах в Телеграмме и в ВК.

Для этого воспользуйтесь [инстркуцией](ttps://cloud.google.com/dialogflow/es/docs/quick/build-agent)

Не забудьте выставить русский язык, иначе бот не будет понимать клиентов.

`*СКРИН*`

Натренируйте бота на нужные вам вопросы в консоли DialogFlow, в разделе Intents или с помощью скрипта `create_indent.py`

`*СКРИН*`

### Обучение DialogFlow по API

В файле ``question.json`` пример как заполнять вопросы.

Запустите скрипт

```bash
python create_intent.py
```

### Получение токена для работы с API DialogFlow

[Включите API DialogFlow на вашем Google-аккаунте](https://cloud.google.com/dialogflow/es/docs/quick/setup#api)

Получите файл `credentials.json` с помощью консольной утилитой gcloud
    
Скачайте на свой компьютер архив с [утилитой](https://cloud.google.com/sdk/docs/install)

Разархивируйте на компьютер

Перейдите в каталог с разархивированной утилитой и запустите инсталлятор:

```bash
./google-cloud-sdk/install.sh
```

Запустите утилиту
```bash
gcloud init

gcloud auth application-default login
```

При запуске попросит верификацию в аккаунт google

После вы получите файл credentials.json к себе на компьютер. Каталог будет указан в ответе утилиты

`*СКРИН*`

Добавьте путь до файла `application_default_credentials.json` в переменные окружения, переменная `GOOGLE_APPLICATION_CREDENTIALS`.

Получите токен от DialogFlow

Запустите скрипт 

```bash
python get_token_dialog_flow.py
```


## Использование

Для запуска Телеграм бота запустите скрипт

```bash
python tg_bot.python
```

Для запуска VK бота запустите скрипт

```bash
python vk_bot.py
```