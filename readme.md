# User Authentication System

## Setup

Run the setup script for initial set up:

```bash
./setup.sh
```

## Running the Application

```bash
fastapi run --reload app/main.py
```

## For performing db migrations
```
alembic init -t async migrations
```