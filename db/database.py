"""Database connection and initialization."""
import sqlite3
import logging
from pathlib import Path


DB_PATH = Path(__file__).parent.parent / "sqlite.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    conn = sqlite3.Connection(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables."""
    if DB_PATH.exists():
        logging.info("✅ Database already exists")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            word_count INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()
    logging.info("✅ Database initialized")
