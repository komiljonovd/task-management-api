python -m venv venv

source venv/bin/activate # Для Linux/macOS

venv\Scripts\activate # Для Windows

pip install -r requirements.txt

python manage.py makemigrations taskpp

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

http://localhost:8000/swagger/ <-- SWAGGER DOCUMENTATION