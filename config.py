import json
import os
from dotenv import load_dotenv

def load_config():
    """Load the configuration from the .env file."""
    load_dotenv()
    
    sqlitecloud = {
        "connection_string": os.getenv("CONNECTION_STRING"),
        "apikey": os.getenv("API_KEY"),
        "db_name": os.getenv("DB_NAME")
    }
    return sqlitecloud