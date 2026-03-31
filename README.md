# Custom Auth System (DRF)

## 🧭 Overview

В рамках проекта реализуется backend-приложение с **кастомной системой аутентификации и авторизации** без использования встроенных механизмов Django.

В качестве архитектурного подхода выбраны:

* **stateful token-based authentication (сессии в БД)** — для явного управления жизненным циклом авторизации (login/logout, инвалидирование)
* **RBAC (Role-Based Access Control)** — для гибкого разграничения прав доступа
* **Layered Architecture (DAL + Service Layer + API)** — для разделения ответственности и масштабируемости
* **Dependency Injection через фабрики** — для снижения связанности и повышения тестируемости

Основной акцент сделан на проектировании системы доступа и архитектуры, а не на использовании готовых решений “из коробки”.

---

## 🏗️ Architecture

### 📦 Project Structure

```
custom_auth_system/
├── config/                  # настройки проекта (settings, urls)
├── auth_app/                # аутентификация и пользователи
├── permissions_app/         # RBAC (роли и права)
├── business_app/            # mock бизнес-ресурсы
├── core/                    # middleware, DI container
├── manage.py
```

---

### 🔷 Layered Architecture

Проект разделён на слои:

* **Repository (DAL)** — доступ к БД (только ORM)
* **Service Layer** — бизнес-логика
* **Serializer** — валидация данных
* **View** — обработка HTTP-запросов

Поток выполнения:

```
View → Service → Repository → Database
```

---

### 🔷 Dependency Injection

Зависимости внедряются через фабрики в `core/container.py`.

Пример:

```python
def get_auth_service():
    return AuthService(
        user_repository=UserRepository(),
        session_repository=SessionRepository()
    )
```

View получают сервисы через container, не создавая зависимости напрямую.

---

## 🔐 Authentication

Реализована **кастомная система аутентификации**.

### Особенности:

* собственная модель пользователя
* собственная модель сессии (token)
* кастомный middleware
* ручная реализация login/logout

### Почему выбран stateful подход:

* простой и управляемый logout
* возможность инвалидировать сессии
* прозрачная логика авторизации

---

## 🔑 Authorization (RBAC)

Реализована ролевая модель доступа:

```
User → Role → Permission → (resource, action)
```

### Сущности:

* User
* Role
* Permission
* UserRole
* RolePermission

### Проверка доступа:

* сервис `check_permission`
* декоратор `@permission_required(resource, action)`

---

## 🚫 Что НЕ использовалось

В проекте намеренно не используются:

* `django.contrib.auth`
* стандартная модель User
* DRF authentication classes
* DRF permission classes

Вся логика реализована вручную.

---

## ✅ Реализованный функционал

* регистрация пользователя
* login / logout
* middleware аутентификации
* soft delete пользователя
* базовая RBAC модель
* проверка прав доступа
* декоратор для защиты endpoint’ов

---

## 🔧 В разработке

* admin API для управления:

  * ролями
  * правами
  * назначением ролей
* mock бизнес endpoints
* seed данных
* унификация ошибок

---

## 🔄 Возможности расширения

Архитектура позволяет:

* заменить stateful auth на JWT (stateless)
* добавить кэширование прав
* расширить RBAC (например, hierarchical roles)

---

## ▶️ Запуск проекта

```Пока только pytest
```

---

## 📌 Примечание

Основная цель проекта — продемонстрировать:

* понимание различий между аутентификацией и авторизацией
* умение проектировать систему доступа
* владение архитектурными подходами (DAL, Service Layer, DI)
* способность реализовывать кастомные решения без reliance на framework abstractions
