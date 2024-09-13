import sqlitecloud
from config import load_config


def get_db_connection():
    """Create and return the database connection using the configuration."""
    config = load_config()

    connection_string = config["sqlitecloud"]["connection_string"]
    apikey = config["sqlitecloud"]["apikey"]
    db_name = config["sqlitecloud"]["db_name"]

    full_connection_string = f"{connection_string}?apikey={apikey}"
    conn = sqlitecloud.connect(full_connection_string)
    conn.execute(f"USE DATABASE {db_name}")

    return conn


def save_data(conn, weight, height, age, gender, protein, calories, result_text):
    """Insert the calculated BMR data into the database."""
    cursor = conn.cursor()

    # Ensure table creation if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL,
            height REAL,
            age INTEGER,
            gender TEXT,
            protein REAL,
            calories REAL,
            result TEXT
        );
    """)

    # Save the data
    cursor.execute("""
        INSERT INTO data (weight, height, age, gender, protein, calories, result) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (weight, height, age, gender, protein, calories, result_text))

    conn.commit()


def load_latest_data(conn):
    """Fetch and return the latest data entry from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()

    if row:
        return row
    else:
        return None
