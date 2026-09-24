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

<p align="center">
  <b>English</b> | <a href="#-русская-версия-russian-version">🇷🇺 Русский (см. ниже / see below)</a>
</p>

---

## 📖 About

**House Rental API** is a backend service for a real estate rental platform developed as an **educational study project**. The project demonstrates a modern RESTful API architecture built with Python: user authentication, relational database modeling, internal wallet balance transactions, house booking logic, and a star-rating review system.

The entire backend, database models, business logic, and Docker containerization were developed from scratch.

---

## ✨ Main Features

| Area | Features |
| :--- | :--- |
| 👤 **Users & Auth** | Registration, JWT Bearer authorization, user profiles, account deletion |
| 💰 **Balance & Wallet** | Real-time balance checking, wallet top-up functionality |
| 🏠 **House Listings** | Create, view (with basket & rental status indicators), edit, and delete house posts |
| 🛒 **Basket** | Add or remove rental listings to/from a personal basket |
| 🔑 **Rental System** | Rent houses (automatic fund transfer from renter to owner balance), active rental tracking, cancellation with refund support |
| ⭐ **Feedback & Ratings** | Post reviews with star ratings (1 to 5 stars), edit/delete feedback, view listing reviews |
| 🐳 **DevOps & Config** | Docker & Docker Compose setup, `.env` file environment configuration |

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python + FastAPI** | High-performance Web Framework for REST API |
| **PostgreSQL + SQLAlchemy** | Relational Database & ORM |
| **Pydantic** | Data validation, serialization, and settings management |
| **PyJWT + pwdlib (Argon2)** | Token-based authentication and secure password hashing |
| **Uvicorn** | ASGI server |
| **Docker / Docker Compose** | Multi-container orchestration (Backend + PostgreSQL) |
| **`.env`** | Secrets and environment variables management |

---

## 🗂️ Project Structure

```text
house-rental/
├── database.py         # Database connection & SessionLocal dependency
├── security.py         # Password hashing (Argon2) & JWT token handling
├── models.py           # SQLAlchemy ORM models (User, Post, Basket, Rental, Feedback)
├── schemas.py          # Pydantic schemas for request validation & responses
├── main.py             # FastAPI entry point and route definitions
├── requirements.txt    # Python dependencies
├── Dockerfile          # Backend containerization configuration
├── docker-compose.yml  # Multi-container service setup (DB + Backend)
├── .env                # Environment variables & database credentials
└── README.md           # Project documentation
```

---

## 🗄️ Database Entity Schema

Core entities and relationships:

```text
User
 ├── Posts (Author)
 ├── Feedbacks (Author)
 ├── Basket Items
 └── Active Rentals

Post (House Listing)
 ├── Author (User)
 ├── Basket Entries
 ├── Rentals
 └── Feedbacks (1 to 5 stars)
```

---

## 🌐 API Endpoints

### 🔑 Authentication & Users

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Authenticate user and receive JWT access token |
| `GET` | `/users/me` | Fetch current user profile |
| `GET` | `/users/{user_id}` | Fetch user details by ID |
| `DELETE` | `/users/delete_account` | Delete user account and associated data |

### 💰 Wallet & Balance

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/users/me/balance` | Check current user balance |
| `POST` | `/users/me/up-top` | Top up user wallet balance |

### 🏠 Listings (Posts)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/posts/create/` | Create a new house rental post |
| `GET` | `/posts/` | Get all posts (includes basket & active rental flags) |
| `PATCH` | `/posts/{post_id}` | Edit post (title, description, price) |
| `DELETE` | `/posts/{post_id}` | Delete a house post |

### 🛒 Basket & 🔑 Rental Logic

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/basket` | View items in current user's basket |
| `POST` | `/basket/{post_id}/in` | Toggle item in/out of basket |
| `GET` | `/rent/check` | View listings currently rented by user |
| `POST` | `/basket/{post_id}/rent` | Rent a house (deducts funds from renter, credits owner) |
| `DELETE` | `/basket/{post_id}/cancel_rent` | Cancel rental (refunds money if rental is active) |

### ⭐ Feedback & Reviews

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/posts/{post_id}/feedback` | Submit a review with star rating (1-5) |
| `PATCH` | `/posts/{post_id}/feedback/{feedback_id}` | Edit feedback text or rating |
| `DELETE` | `/posts/{post_id}/feedback/{feedback_id}` | Delete feedback |
| `GET` | `/posts/{post_id}/feedbacks` | Fetch all reviews for a listing |

---

## 🚀 Run Locally

### Requirements

* Python 3.11+
* Docker & Docker Compose

### Environment Setup

Create a `.env` file in the root directory:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=house_rental_db
SECRET_KEY=your_super_secret_jwt_key_here
```

### Run with Docker Compose

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

## 📚 Interactive API Documentation

Once the backend is running, access the interactive API docs at:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎯 Learning Goals

```text
REST API Architecture
  ↓
JWT Authentication & Argon2 Password Hashing
  ↓
SQLAlchemy ORM & Complex Relational Models
  ↓
Transactional Logic (Wallet Balances & Booking Management)
  ↓
Docker Containerization & Environment Orchestration
```

---

## ⚠️ Educational Project

This project was built for **educational and portfolio purposes**.

For a production environment, it would benefit from database migrations (Alembic), background job processing for expired rentals (Celery/APScheduler), Redis caching, rate limiting, and tighter CORS policies.

---

<br>

<a name="-русская-версия-russian-version"></a>
<details>
<summary><b>🇷🇺 Нажмите здесь, чтобы открыть описание на русском языке (Russian Version)</b></summary>

<br>

### 📖 О проекте

**House Rental API** — это бэкенд-сервис для платформы аренды недвижимости, разработанный в качестве **учебного проекта**. Проект демонстрирует архитектуру REST API с использованием современного стека Python: аутентификация пользователей, связи в реляционной базе данных, внутренние финансовые транзакции баланса, логика аренды и система отзывов с рейтингом.

---

### ✨ Основной функционал

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

### 🛠️ Технологический стек

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

### 🚀 Инструкция по локальному запуску

#### Настройка окружения

Создайте файл `.env` в корневом каталоге проекта:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=house_rental_db
SECRET_KEY=your_super_secret_jwt_key_here
```

#### Запуск через Docker Compose

```bash
docker compose up --build
```

Остановка контейнеров:

```bash
docker compose down
```

</details>

---

<p align="center">

<strong>Built with Python & FastAPI. Built to learn.</strong>

</p>