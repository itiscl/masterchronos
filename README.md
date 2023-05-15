# Инструкция по запуску для Linux

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
