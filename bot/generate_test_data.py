"""Generate test data for CensorRace."""
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "sqlite.db"

# Тестові фрази з буквою "а"
test_phrases = [
    "Так, давай зробимо",
    "Класно працює",
    "Дякую за допомогу",
    "Чудова ідея",
    "Зараз перевірю",
    "Все працює нормально",
    "Треба додати функцію",
    "Гарна робота",
    "Давай спробуємо",
    "Відмінно виглядає"
]

def generate_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Генеруємо дані за останні 48 годин
    now = datetime.now()
    user_ids = [290363608167350282, 123456789012345678, 987654321098765432]
    
    records_added = 0
    
    for hour_offset in range(48):
        timestamp = now - timedelta(hours=hour_offset)
        
        # 3-7 записів на годину
        records_per_hour = random.randint(3, 7)
        
        for _ in range(records_per_hour):
            user_id = random.choice(user_ids)
            text = random.choice(test_phrases)
            
            # Рахуємо букву "а" (кирилиця)
            word_count = text.lower().count('а')
            
            # Додаємо невелику випадкову затримку в межах години
            minute_offset = random.randint(0, 59)
            record_time = timestamp - timedelta(minutes=minute_offset)
            
            cursor.execute("""
                INSERT INTO transcriptions (user_id, timestamp, text, word_count)
                VALUES (?, ?, ?, ?)
            """, (user_id, record_time, text, word_count))
            
            records_added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Generated {records_added} test records for last 48 hours")
    print(f"📊 Users: {len(user_ids)}")
    print(f"🔤 Tracking letter: 'а'")

if __name__ == "__main__":
    generate_data()
