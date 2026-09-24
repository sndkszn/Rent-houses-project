# House Rental API

<p align="center">

  <strong>Backend Service for Real Estate Rental Platform</strong><br>
  <sub>Educational / Study Portfolio Project</sub>

</p>

<p align="center">

  <img src="https://img.shields.io/badge/Project-Educational-orange?style=for-the-badge&logo=readme&logoColor=white" alt="Educational Project">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">

</p>

---

## 📖 About

**House Rental API** — это бэкенд-сервис для платформы аренды недвижимости, разработанный в качестве **учебного проекта**. Проект демонстрирует архитектуру REST API с использованием современного стека Python: аутентификация пользователей, связи в реляционной базе данных, внутренние финансовые транзакции баланса, логика аренды и система отзывов с рейтингом.

Весь бэкенд, модели баз данных, бизнес-логика и контейнеризация созданы вручную.

---

## ✨ Main Features

| Область | Функционал |
| :--- | :--- |
| 👤 **Users & Auth** | Регистрация, авторизация по JWT Bearer, просмотр профилей, удаление аккаунта |
| 💰 **Balance & Wallet** | Проверка баланса в реальном времени, система пополнения счета |
| 🏠 **House Listings** | Создание, просмотр (со статусами аренды и корзины), редактирование и удаление объявлений |
| 🛒 **Basket** | Добавление и удаление объявлений из личной корзины |
| 🔑 **Rental System** | Аренда домов (авто-перевод средств с баланса арендатора владельцу), отслеживание активной аренды, отмена аренды с возвратом денег |
| ⭐ **Feedback & Ratings** | Отзывы с рейтингом (от 1 до 5 звезд), редактирование/удаление отзывов, просмотр отзывов к объекту |
| 🐳 **DevOps & Config** | Docker & Docker Compose сборка, управление конфигурацией через `.env` |

---

## 🛠️ Tech Stack

| Технология | Назначение |
| :--- | :--- |
| **Python + FastAPI** | Высокопроизводительный фреймворк для REST API |
| **PostgreSQL + SQLAlchemy** | Реляционная БД и ORM для работы с данными |
| **Pydantic** | Валидация данных, сериализация и схемы |
| **PyJWT + pwdlib (Argon2)** | Аутентификация по токенам и надежное хеширование паролей |
| **Uvicorn** | ASGI-сервер для запуска FastAPI |
| **Docker / Docker Compose** | Мультиконтейнерная оркестрация (Бэкенд + PostgreSQL) |
| **`.env`** | Хранение секретов и переменных окружения |

---

## 🗂️ Project Structure

```text
house-rental/
├── database.py         # Подключение к БД и зависимость SessionLocal
├── security.py         # Хеширование паролей (Argon2) и работа с JWT токенами
├── models.py           # Модели SQLAlchemy (User, Post, Basket, Rental, Feedback)
├── schemas.py          # Схемы Pydantic для валидации запросов и ответов
├── main.py             # Точка входа FastAPI и эндпоинты
├── requirements.txt    # Зависимости проекта
├── Dockerfile          # Сборка контейнера для бэкенда
├── docker-compose.yml  # Запуск мультиконтейнерного окружения (БД + бэкенд)
├── .env                # Переменные окружения (ключи, доступы к БД)
└── README.md           # Документация проекта
```

---

## 🗄️ Database Entity Schema

Основные сущности и связи:

```text
User
 ├── Posts (Автор)
 ├── Feedbacks (Автор)
 ├── Basket Items
 └── Active Rentals

Post (Объявление)
 ├── Author (User)
 ├── Basket Entries
 ├── Rentals
 └── Feedbacks (от 1 до 5 звезд)
```

---

## 🌐 API Endpoints

### 🔑 Authentication & Users

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `POST` | `/register` | Регистрация нового пользователя |
| `POST` | `/login` | Авторизация и получение JWT-токена |
| `GET` | `/users/me` | Получение профиля текущего пользователя |
| `GET` | `/users/{user_id}` | Получение профиля пользователя по ID |
| `DELETE` | `/users/delete_account` | Удаление аккаунта и связанных данных |

### 💰 Wallet & Balance

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `GET` | `/users/me/balance` | Проверка баланса |
| `POST` | `/users/me/up-top` | Пополнение баланса |

### 🏠 Listings (Posts)

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `POST` | `/posts/create/` | Создание объявления |
| `GET` | `/posts/` | Получение всех объявлений (с флагами корзины и аренды) |
| `PATCH` | `/posts/{post_id}` | Редактирование объявления (заголовок, текст, цена) |
| `DELETE` | `/posts/{post_id}` | Удаление объявления |

### 🛒 Basket & 🔑 Rental Logic

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `GET` | `/basket` | Просмотр объявлений в корзине |
| `POST` | `/basket/{post_id}/in` | Добавление / удаление из корзины |
| `GET` | `/rent/check` | Просмотр арендованных пользователем домов |
| `POST` | `/basket/{post_id}/rent` | Аренда дома (списание средств у арендатора и зачисление владельцу) |
| `DELETE` | `/basket/{post_id}/cancel_rent` | Отмена аренды (с возвратом средств, если она активна) |

### ⭐ Feedback & Reviews

| Метод | Эндпоинт | Описание |
| :--- | :--- | :--- |
| `POST` | `/posts/{post_id}/feedback` | Оставить отзыв с оценкой (1–5 звезд) |
| `PATCH` | `/posts/{post_id}/feedback/{feedback_id}` | Редактировать текст или рейтинг отзыва |
| `DELETE` | `/posts/{post_id}/feedback/{feedback_id}` | Удалить отзыв |
| `GET` | `/posts/{post_id}/feedbacks` | Получить все отзывы к объявлению |

---

## 🚀 Run Locally

### Требования

* Python 3.11+
* Docker & Docker Compose

### Настройка окружения

Создайте файл `.env` в корневом каталоге проекта:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=house_rental_db
SECRET_KEY=your_super_secret_jwt_key_here
```

### Запуск через Docker Compose

```bash
docker compose up --build
```

Остановка контейнеров:

```bash
docker compose down
```

---

## 📚 Interactive API Documentation

После запуска бэкенда интерактивная документация доступна по адресам:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎯 Learning Goals

```text
REST API Architecture
  ↓
JWT Authentication & Argon2 Password Hashing
  ↓
SQLAlchemy ORM & Complex DB Relations
  ↓
Transactional Logic (Balance Transfer & Rental Management)
  ↓
Docker Containerization & Environment Orchestration
```

---

## ⚠️ Educational Project

Проект создан в **учебных и портфолио целях**.

Для подготовки к продакшену рекомендуется добавить миграции базы данных (Alembic), фоновые задачи для очистки истекших аренд (Celery/APScheduler), кэширование в Redis, ограничение количества запросов (Rate Limiting) и более строгие политики CORS.

---

<p align="center">

<strong>Built with Python & FastAPI. Built to learn.</strong>

</p>