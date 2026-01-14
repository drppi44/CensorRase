"""Database repository functions."""
from datetime import datetime
from db.database import get_connection
from db.models import Transcription


def insert_transcription(user_id: int, text: str, word_count: int) -> int:
    """Insert new transcription record."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO transcriptions (user_id, text, word_count)
        VALUES (?, ?, ?)
    """, (user_id, text, word_count))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    
    return record_id


def get_user_stats(user_id: int) -> dict:
    """Get statistics for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_records,
            SUM(word_count) as total_words
        FROM transcriptions
        WHERE user_id = ?
    """, (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return {
        "total_records": row["total_records"],
        "total_words": row["total_words"] or 0
    }


def get_leaderboard(limit: int = 10) -> list[dict]:
    """Get leaderboard of users by word count."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            user_id,
            SUM(word_count) as total_words,
            COUNT(*) as total_records
        FROM transcriptions
        GROUP BY user_id
        ORDER BY total_words DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
