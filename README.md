# verb_games_sup_bot

Чат-бот для Telegram и [ВКонтакте](https://vk.com/), созданный на основе Google Dialogflow. 
Бот использует обработку естественного языка (NLP) для понимания запросов пользователей 
и автоматического ответа.
![TG-BOTS](https://github.com/user-attachments/assets/41527c25-4e0a-4a8d-94f4-f2f3ed1016d6)



## Как запустить 

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

`GOOGLE_APPLICATION_CREDENTIALS` - Путь до credentials.json полученный при запуске и инициализации GoogleCLI,

Для **Продакшена**, скопируйте файл `GOOGLE_APPLICATION_CREDENTIALS.json` в корень проекта на сервер
Перейдите в католог, где расположен файл `GOOGLE_APPLICATION_CREDENTIALS.json` на вашем компьютере и выполните  команду

```
scp ПУТЬ_ДО_ФАЙЛА/GOOGLE_APPLICATION_CREDENTIALS.json root@your-server:/opt/verb_games_sup_bot
```

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

![ОКНО ПРОЕКТА DialogFlow](https://github.com/user-attachments/assets/c2601dac-a070-4109-b7fb-84875902f0eb)

Нам должны выдать такой идентификатор 

```
НАЗВАНИЕ ВАШЕГО ПРОЕКТА-211973
```


### Создайте агента и натренируйте его

Агент - это бот, который будет отвечать на вопросы пользователей и будем использовать его в своих ботах в Телеграмме и в ВК.

[Для этого воспользуйтесь инструкцией](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)

Не забудьте выставить русский язык, иначе бот не будет понимать клиентов.

Натренируйте бота на нужные вам вопросы в консоли DialogFlow, в разделе Intents или с помощью скрипта `create_indent.py`

![ Агент Dialogflow](https://github.com/user-attachments/assets/eecad355-b98a-4244-be5c-b7ab80db4f32)


### Получение токена для работы с API DialogFlow

[Включите API DialogFlow на вашем Google-аккаунте](https://cloud.google.com/dialogflow/es/docs/quick/setup#api)

Получите файл `credentials.json` с помощью консольной утилитой gcloud
    
Скачайте на свой компьютер архив с [утилитой](https://cloud.google.com/sdk/docs/install)

Разархивируйте на компьютер

Перейдите в каталог с разархивированной утилитой и запустите инсталлятор

```bash
./google-cloud-sdk/install.sh
```

Установщик внёс изменения в .bashrc, применяем их:

```bash
source ~/.bashrc
```

Запустите утилиту
```bash
gcloud init

gcloud auth application-default login
```

При запуске скрипта, он опросит верификацию в аккаунт google

После вы получите файл credentials.json к себе на компьютер. 
Папка где располагается файл с токеном будет указан в ответе утилиты

Добавьте путь до файла `application_default_credentials.json` в переменные окружения,
переменная `GOOGLE_APPLICATION_CREDENTIALS`.


### Обучение DialogFlow по API

В файле `question.json` пример как заполнять вопросы.

Запустите скрипт

```bash
python create_intent.py
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
