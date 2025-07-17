# Инструкция по развертыванию Flask-проекта

## 1. Обновление системы и установка базовых пакетов

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nginx curl build-essential libpq-dev
```

## 2. Установка и настройка PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

## 3. Создание базы данных и пользователя PostgreSQL

```bash
sudo -u postgres psql
```

В открывшейся консоли Postgres:

```sql
CREATE DATABASE flask_db;
CREATE USER flask_user WITH PASSWORD 'flask_pass';
ALTER ROLE flask_user SET client_encoding TO 'utf8';
ALTER ROLE flask_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE flask_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE flask_db TO flask_user;
\q
```

## 4. Клонирование проекта

```bash
git clone https://github.com/grisha-topolev/grab20.git
cd grab20
```

## 5. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

## 6. Установка зависимостей проекта

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 7. Настройка переменных окружения

```bash
cat <<EOF > .env
DB_NAME=flask_db
DB_USER=flask_user
DB_PASS=flask_pass
DB_HOST=localhost
DB_PORT=5432
EOF
```

## 8. Применение миграций базы данных

```bash
flask db upgrade
```

## 9. Установка Gunicorn

```bash
pip install gunicorn
```

## 10. Проверка запуска приложения через Gunicorn (TCP)

```bash
gunicorn --workers 3 --bind 127.0.0.1:8000 run:app
```

## 11. Настройка сервиса systemd для Gunicorn

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Вставить следующее (замени `/home/ubuntu/grab20` на свой путь, ubuntu - имя пользователя):

```ini
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ubuntu/grab20
Environment="PATH=/home/ubuntu/grab20/venv/bin"
ExecStart=/home/ubuntu/grab20/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 run:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
```

## 12. Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/flaskapp
```

Вставить:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 13. Проверка результата

Откройте в браузере:

```
http://<ip_адрес_сервера>
```

✅ После этих шагов вы получите полностью работающий Flask-проект, развернутый на Gunicorn + Nginx через TCP-порт, с базой данных PostgreSQL.
