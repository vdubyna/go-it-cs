import psycopg2

# Database connection configuration
DB_CONFIG = {
    'dbname': 'goit',
    'user': 'goit',
    'password': 'goit',
    'host': 'localhost',
    'port': 5432
}

# SQL statements to create the tables
CREATE_TABLES_SQL = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

def create_tables():
    try:
        # Establish connection to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the SQL to create tables
        cursor.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("Tables created successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()