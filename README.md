# Document Searcher
## Быстрый старт
- Используйте `.env файл`. Вы можете скопировать `.env.example`
- Используйте `python3 -m venv ./.venv && source ./.venv/bin/activate && pip install -r requirements.txt` 
- Запустите команду `docker compose up -d --build`
- Выполните миграции `docker exec app_searcher alembic upgrade head`

## Запуск тестов
- Выполните команду в корневом каталоге проекта `pytest ./tests` <br> Если будет возникать ошибка `ModuleNotFoundError: No module named 'app'`, то вам необходимо прописать в консоль `export PYTHONPATH=/path/to/this/project`, где в качестве путя должен быть путь до этого проекта <br >Запуск тестов не требует поднятия докера.

## Описание приложения
Данное приложение является простым поисковиком по текстам документов. Данные хранятся в БД и индексе elastcsearch.
API методы:
- `/api/add/` - добавление документа в БД и индекс elastcsearch.
- `/api/delete/` - удаление документа из БД и индекса elasticsearch
- `/api/search/` - поиск паттерна в индексе elasticsearch и возвращение первых 20 документов