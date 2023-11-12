#!/bin/sh

if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(cat .env | xargs)
fi

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py collectstatic --noinput

echo "from users.models import User;
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser(
        '$DJANGO_SUPERUSER_EMAIL',
        '$DJANGO_SUPERUSER_PASSWORD',
    )" | python3 manage.py shell

uwsgi --ini /web/arsy.uwsgi.ini
