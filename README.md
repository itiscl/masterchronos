# Инструкция по запуску в Linux

1. git clone https://github.com/itiscl/masterchronos.git
2. cd masterchronos
3. python3 -m venv .venv
4. source .venv/bin/activate
5. python3 -m pip install --upgrade pip
6. python3 -m pip install django
7. python3 -m django --version
8. python3 manage.py makemigrations timesheet
9. python3 manage.py migrate
10. python3 manage.py createsuperuser
11. python3 manage.py runserver

# Инструкция по запуску в Windows (PowerShell)

1. git clone https://github.com/itiscl/masterchronos.git
2. cd masterchronos
3. python -m venv .venv
4. .\.venv\Scripts\Activate.ps1
5. python -m pip install --upgrade pip
6. python -m pip install django
7. python -m django --version
8. python manage.py makemigrations timesheet
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py runserver

# Инструкции после запуска сервера Django

1. В панели администрирования http://127.0.0.1/admin/ добавить сотрудников и активности.
2. Вернуться на главную страницу http://127.0.0.1/
