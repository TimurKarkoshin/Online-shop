## Как установить
Для работы сервиса требуются:
- Python >= 3.10.
- ПО для контейнеризации - [Docker](https://docs.docker.com/engine/install/).
- Инструмент [poetry](https://python-poetry.org/) для управления зависимостями и сборкой пакетов в Python.

Настройка переменных окружения
1. Скопируйте файл .env.dist в .env
2. Заполните .env файл. Пример:
```yaml
DATABASE_URL = postgresql://skillbox:secret@127.0.0.1:5434/market
REDIS_URL = redis://127.0.0.1:6379/0
```

Запуск СУБД Postgresql
```shell
docker run --name skillbox-db -e POSTGRES_USER=skillbox -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=market -p 5434:5432 -d postgres
```
Запуск брокера сообщений REDIS
```shell
docker run --name redis-db -d redis
```
Установка и активация виртуального окружения
```shell
poetry install  ; установка пакетов
poetry shell  ; активация виртуального окружения
pre-commit install  ; установка pre-commit для проверки форматирования кода, см. .pre-commit-config.yaml
```
### Как удалить контейнеры
СУБД Postgres
```
docker rm -f -v skillbox-db
```

Брокер сообщений REDIS
```
docker rm -f -v redis-db
```

## Проверка форматирования кода
Проверка кода выполняется из корневой папки репозитория.
* Анализатор кода flake8
```shell
flake8 market
```
* Линтер pylint
```shell
pylint --rcfile=.pylintrc market/*
```
* Линтер black
```shell
black market
```

## Как запустить web-сервер
Запуск сервера производится в активированном локальном окружение из папки `market/`
```shell
python manage.py runserver 0.0.0.0:8000
```
## Добавление пользователей в модели User и Profile
После создания проекта выполнете миграции и запустите СУБД.
Запуск команды производится из папки `market/`
```shell
python manage.py add_new_users
```

## Запуск файла импорта в рамках задачи в другом процессе
Чтобы импорт товаров из файла запускался в другом процессе и не нагружал основной процесс,
нужно запустить celery в дополнительных терминалах

1 терминал
```shell
celery -A config worker -l info
```
2 терминал
```shell
celery -A config beat -l info
```
Если нужно какой-либо файл отправить без очереди, то нужно воспользоваться командой.
Можно указать только email, только название файла для импорта, либо и то и другое
```shell
python manage.py import_yaml --file filename.yaml --email example@mail.com
```

## Внешнее оформление

<details> 
  <summary>Внешний вид главной страницы</summary>
   ![Main page](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/9287cef1-328a-4659-9aa9-8f7ae4c0cb3e)
</details>

<details> 
  <summary>Страничка профиля</summary>
   ![Profile](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/3e23e3d0-dc2f-4dc6-88a2-08db44314dad)
</details>

<details> 
  <summary>Каталог</summary>
    ![Catalog](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/edfb64d2-80ed-4cbc-a7b5-8b85fa6b0d85)
</details>

<details> 
  <summary>Детальная страница товара</summary>
   ![Product detail](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/2f3f057a-c718-461e-b112-9f6ec648247a)
</details>

<details> 
  <summary>Корзина</summary>
   ![Basket](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/a510bb5d-013d-4f72-aece-e42a662f1d10)
</details>

<details> 
  <summary>Оформление заказа</summary>
   ![Order](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/aebda507-c08e-49cf-972d-6c600131286a)
</details>

<details> 
  <summary>Детальная страница магазина</summary>
   ![Shop](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/4e582480-ae34-4e6e-a782-a68bf614aa24)
</details>

<details> 
  <summary>Расширяемая CMS сайта</summary>
   ![CMS](https://github.com/TimurKarkoshin/Online-shop/assets/144448914/0b8681c4-2401-4bf0-96b3-2ac3d96dedcf)
</details>
