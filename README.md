# 🏁 CensorRace

**Discord voice chat profanity tracker and leaderboard**

A Discord bot that records voice conversations, transcribes them using Whisper AI, counts profanity usage, and stores statistics in a database.

## 🎯 Features

- 🎤 **Continuous voice recording** - Records Discord voice channel in chunks
- 🤖 **AI transcription** - Uses Faster-Whisper (tiny model) for speech-to-text
- 📊 **Profanity tracking** - Counts specific words and stores in SQLite database
- 🔄 **Auto-reconnect** - Handles Discord disconnections gracefully
- 💾 **Database storage** - Tracks user statistics over time

## 📁 Project Structure

```
CensorRace/
├── main.py                 # Discord bot main loop
├── constants.py            # Configuration from .env
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── censorrace.db          # SQLite database (auto-created)
├── asr/
│   └── whisper_engine.py  # Whisper transcription
├── db/
│   ├── database.py        # Database connection
│   ├── models.py          # Data models
│   └── repository.py      # Database queries
├── audio/
│   └── temp/              # Temporary audio files
└── models/
    └── faster-whisper-tiny/  # Whisper model
```

## 🚀 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create `.env` file:

```env
DIS_TOKEN=your_discord_bot_token
DIS_VOICE_CHANNEL_ID=your_voice_channel_id
WORD=word_to_track
RECORD_DURATION_SECONDS=10
```

### 3. Download Whisper model

Place `faster-whisper-tiny` model in `models/` directory.

### 4. Run the bot

```bash
python main.py
```

## 🗄️ Database Schema

**Table: `transcriptions`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Discord user ID |
| timestamp | DATETIME | When recorded |
| text | TEXT | Transcribed text |
| word_count | INTEGER | Profanity count |

## 🛠️ Tech Stack

- **py-cord** - Discord API wrapper
- **faster-whisper** - Speech recognition
- **SQLite** - Database
- **asyncio** - Async event loop

## 📝 How It Works

1. Bot connects to Discord voice channel
2. Records audio in chunks (configurable duration)
3. Saves audio files to `audio/temp/`
4. Transcribes audio using Whisper AI
5. Counts target word occurrences
6. Stores results in SQLite database
7. Repeats continuously

## 🔮 Future Plans

- [ ] FastAPI backend for statistics
- [ ] React/Vue frontend with charts
- [ ] Leaderboard visualization
- [ ] Docker deployment
- [ ] Multi-word tracking
- [ ] Username resolution

## 📄 License

MIT