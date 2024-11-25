from faker import Faker
import psycopg2
from random import randint

# Конфігурація підключення до бази даних PostgreSQL
DB_CONFIG = {
    'dbname': 'goit',
    'user': 'goit',
    'password': 'goit',
    'host': 'localhost',
    'port': 5432
}

def insert_data_to_db(users, statuses, tasks):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Вставляємо користувачів
        cursor.executemany(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            users
        )

        # Вставляємо статуси
        cursor.executemany(
            "INSERT INTO status (name) VALUES (%s)",
            statuses
        )

        # Вставляємо завдання
        cursor.executemany(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            tasks
        )

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fake = Faker()

    # Генеруємо користувачів
    users = [(fake.name(), fake.unique.email()) for _ in range(10)]

    # Генеруємо статуси
    statuses = [('new',), ('in progress',), ('completed',)]

    # Генеруємо завдання
    tasks = [
        (
            fake.sentence(nb_words=5),
            fake.text(),
            randint(1, len(statuses)),  # Випадковий статус
            randint(1, len(users))     # Випадковий користувач
        )
        for _ in range(20)
    ]

    insert_data_to_db(users, statuses, tasks)