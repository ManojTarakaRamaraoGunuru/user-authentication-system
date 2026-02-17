#!/usr/bin/env python3

import sys
import subprocess


def run_server():
    subprocess.run(
        ["fastapi", "run", "--reload", "app/main.py"],
        check=True
    )


def make_migration(message):
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=True
    )


def upgrade():
    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True
    )


def downgrade():
    subprocess.run(
        ["alembic", "downgrade", "head"],
        check=True
    )


def main():
    if len(sys.argv) < 2:
        print("""
Usage:
  python manage.py runserver
  python manage.py makemigrations "message"
  python manage.py upgrade
  python manage.py downgrade
""")
        return

    command = sys.argv[1]

    if command == "runserver":
        run_server()

    elif command == "makemigrations":
        if len(sys.argv) < 3:
            print("Provide migration message.")
            return
        make_migration(sys.argv[2])

    elif command == "upgrade":
        upgrade()

    elif command == "downgrade":
        downgrade()

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
