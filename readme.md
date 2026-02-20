# User Authentication System

## Setup

Run the setup script for initial set up:

```bash
./setup.sh
```

## Running the Application

Use manage.py to run the application accordingly
```
  python manage.py runserver
  python manage.py makemigrations "message" 
  python manage.py upgrade
  python manage.py downgrade
```

To run the application delibrately without manage.py
```bash
fastapi run --reload app/main.py
```

## For performing db migrations
```
alembic init -t async migrations
```
```
alembic revision --autogenerate -m "init"
```
```
alembic upgrade head
```