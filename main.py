'''
Подготовка:

    Установите все необходимые библиотеки для дальнейшей работы: fastapi.
    Создайте файлы, структурировав из согласно рисунку:

    Задача "Основные маршруты":
Необходимо создать маршруты и написать Pydantic модели для дальнейшей работы.
Маршруты:
В модуле task.py напишите APIRouter с префиксом '/task' и тегом 'task', а также следующие маршруты, с пустыми функциями:

    get '/' с функцией all_tasks.
    get '/task_id' с функцией task_by_id.
    post '/create' с функцией create_task.
    put '/update' с функцией update_task.
    delete '/delete' с функцией delete_task.

В модуле user.py напишите APIRouter с префиксом '/user' и тегом 'user', а также следующие маршруты, с пустыми функциями:

    get '/' с функцией all_users.
    get '/user_id' с функцией user_by_id.
    post '/create' с функцией create_user.
    put '/update' с функцией update_user.
    delete '/delete' с функцией delete_user.

В файле main.py создайте сущность FastAPI(), напишите один маршрут для неё - '/', по которому функция возвращает словарь - {"message": "Welcome to Taskmanager"}.
Импортируйте объекты APIRouter и подключите к ранее созданному приложению FastAPI, объединив все маршруты в одно приложение.
Схемы:
Создайте 4 схемы в модуле schemas.py, наследуемые от BaseModel, для удобной работы с будущими объектами БД:

    CreateUser с атрибутами: username(str), firstname(str), lastname(str) и age(int)
    UpdateUser с атрибутами: firstname(str), lastname(str) и age(int)
    CreateTask с атрибутами: title(str), content(str), priority(int)
    UpdateTask с теми же атрибутами, что и CreateTask.

Обратите внимание, что 1/2 и 3/4 схемы обладают одинаковыми атрибутами.

Таким образом вы получите подготовленные маршруты и схемы для дальнейшего описания вашего API.
'''
git init
'''
Подготовка:

    Установите все необходимые библиотеки для дальнейшей работы: sqlalchemy.
    Добавьте файлы в ранее созданную структуру проекта согласно рисунку:

Задача "Модели SQLAlchemy":
Необходимо создать 2 модели для базы данных, используя SQLAlchemy.
База данных и движок:
В модуле db.py:

    Импортируйте все необходимые функции и классы , создайте движок указав пусть в БД - 'sqlite:///taskmanager.db' и 
    локальную сессию (по аналогии с видео лекцией).
    Создайте базовый класс Base для других моделей, наследуясь от DeclarativeBase.

Модели баз данных:
В модуле task.py создайте модель Task, наследованную от ранее написанного Base со следующими атрибутами:

    __tablename__ = 'tasks'
    id - целое число, первичный ключ, с индексом.
    title - строка.
    content - строка.
    priority - целое число, по умолчанию 0.
    completed - булевое значение, по умолчанию False.
    user_id - целое число, внешний ключ на id из таблицы 'users', не NULL, с индексом.
    slug - строка, уникальная, с индексом.
    user - объект связи с таблицей с таблицей User, где back_populates='tasks'.

В модуле user.py создайте модель User, наследованную от ранее написанного Base со следующими атрибутами:

    __tablename__ = 'users'
    id - целое число, первичный ключ, с индексом.
    username - строка.
    firstname - строка.
    lastname - строка.
    age - целое число.
    slug - строка, уникальная, с индексом.
    tasks - объект связи с таблицей с таблицей Task, где back_populates='user'.

После описания моделей попробуйте распечатать SQL запрос в консоль при помощи CrateTable (аналогично видео).

    Не забудьте об импорте одного класса модели в модуль с другим, чтобы таблицы были видны друг другу.
    Для более удобного импорта необходимо дополнить __init__.py в пакете models следующими строками:

from .user import User from .task import Task

Таким образом вы получите 2 модели связанные один(User) ко многим(Task).    
'''

#  main.py

from fastapi import FastAPI
from routers.task import router as task_router
from routers.user import router as user_router
# from models.user import User
# from models.task import Task

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task_router)
app.include_router(user_router)
