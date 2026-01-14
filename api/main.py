"""FastAPI server for CensorRace statistics."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Додати батьківську директорію до path для імпорту db модулів
sys.path.append(str(Path(__file__).parent.parent))

from db.repository import get_user_stats, get_leaderboard

app = FastAPI(title="CensorRace API", version="1.0.0")

# CORS для фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "service": "CensorRace API"}


@app.get("/stats/user/{user_id}")
def user_stats(user_id: int):
    """Get statistics for a specific user."""
    stats = get_user_stats(user_id)
    return {
        "user_id": user_id,
        "total_records": stats["total_records"],
        "total_words": stats["total_words"]
    }


@app.get("/stats/leaderboard")
def leaderboard(limit: int = 10):
    """Get leaderboard of top users."""
    return get_leaderboard(limit)


@app.get("/stats/timeline")
def timeline():
    """
    Get word count timeline for last 48 hours, grouped by hour, filtering letter 'а'.
    """
    from db.database import get_connection
    from datetime import datetime, timedelta
    
    conn = get_connection()
    cursor = conn.cursor()
    
    since = datetime.now() - timedelta(hours=48)
    
    query = """
        SELECT 
            strftime('%Y-%m-%d %H:00:00', timestamp) as period,
            SUM(word_count) as total_words
        FROM transcriptions
        WHERE timestamp >= ?
        AND LOWER(text) LIKE '%а%'
        GROUP BY period
        ORDER BY period
    """
    
    cursor.execute(query, (since,))
    rows = cursor.fetchall()
    conn.close()
    
    return [{"period": row["period"], "total_words": row["total_words"]} for row in rows]
