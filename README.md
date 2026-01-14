# 🏁 CensorRace

**Discord voice chat profanity tracker and leaderboard**

A Discord bot that records voice conversations, transcribes them using Whisper AI, counts profanity usage, and stores statistics in a database with a web dashboard.

## 🎯 Features

- 🎤 **Continuous voice recording** - Records Discord voice channel in chunks
- 🤖 **AI transcription** - Uses Faster-Whisper (tiny model) for speech-to-text
- 📊 **Profanity tracking** - Counts specific words/letters and stores in SQLite database
- 🔄 **Auto-reconnect** - Handles Discord disconnections gracefully
- 💾 **Database storage** - Tracks user statistics over time
- 📈 **Web dashboard** - Real-time charts and leaderboard
- 🐳 **Docker support** - Easy deployment with docker-compose

## 📁 Project Structure

```
CensorRace/
├── bot/                    # Discord bot
│   ├── main.py            # Bot main loop
│   ├── constants.py       # Configuration
│   ├── asr/               # Whisper transcription
│   ├── audio/temp/        # Temporary audio files
│   ├── db/                # Database models
│   └── models/            # Whisper model
├── api/                   # FastAPI backend
│   └── main.py           # API endpoints
├── frontend/             # Web dashboard
│   └── index.html        # SPA interface
├── db/                   # Shared database module
├── sqlite.db            # SQLite database (gitignored)
├── docker-compose.yml    # Docker orchestration
└── .env                  # Environment variables
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Create `.env` file:**

```env
DIS_TOKEN=your_discord_bot_token
DIS_VOICE_CHANNEL_ID=your_voice_channel_id
WORD=а
RECORD_DURATION_SECONDS=10
```

2. **Run:**

```bash
docker-compose up -d
```

3. **Access:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Bot

```bash
cd bot
pip install -r requirements.txt
python main.py
```

#### API

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --port 8000
```

#### Frontend

```bash
cd frontend
python3 -m http.server 3000
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
- **FastAPI** - REST API
- **Chart.js** - Data visualization
- **Docker** - Containerization

## 📝 How It Works

1. Bot connects to Discord voice channel
2. Records audio in chunks (configurable duration)
3. Saves audio files to `audio/temp/`
4. Transcribes audio using Whisper AI
5. Counts target word/letter occurrences
6. Stores results in SQLite database
7. API serves data to frontend
8. Frontend displays real-time charts and leaderboard

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

## 📊 API Endpoints

- `GET /` - Health check
- `GET /stats/user/{user_id}` - User statistics
- `GET /stats/leaderboard?limit=10` - Top users
- `GET /stats/timeline` - Timeline chart data (48h, hourly, letter 'а')

## 🔧 Configuration

Edit `.env` file:

- `DIS_TOKEN` - Discord bot token
- `DIS_VOICE_CHANNEL_ID` - Voice channel ID to monitor
- `WORD` - Word or letter to track
- `RECORD_DURATION_SECONDS` - Recording chunk duration

## 🧪 Generate Test Data

```bash
cd bot
python generate_test_data.py
```

Generates ~200-300 test records for last 48 hours.

## 🔮 Future Plans

- [ ] Username resolution
- [ ] Multi-word tracking
- [ ] Advanced filtering
- [ ] Export statistics
- [ ] Notifications
- [ ] Cloud deployment

## 📄 License

MIT

## 🤝 Contributing

Pull requests are welcome!

---

Made with ❤️ for Discord communities
