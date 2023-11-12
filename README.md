# Тестовое задание ARSY

В данном проекте используется DjangoREST Framework, Blender, PostgreSQL, Nginx, Docker.

### Для запуска проекта вам потребуется выполнить следующие комманды:

## Клонирование репозитория

Для начала работы с проектом, склонируйте его себе на локальный компьютер:

```bash
git clone https://github.com/maxcrimea/ARSY.git
cd arsy
```

## Настройка окружения

Создайте файл .env в корневой директории проекта, используя env.example как шаблон.

## Запуск проекта

Для запуска проекта используйте Docker Compose:

```bash
docker-compose up -d
```

После успешного запуска, проект будет доступен по адресу 

Admin панель: http://localhost:8888/admin/

swagger: http://localhost:8888/swagger/

redoc: http://localhost:8888/redoc/
