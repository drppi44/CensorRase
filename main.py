import time

from discord import Intents
from discord.ext import commands
from discord.sinks import WaveSink
import asyncio

from faster_whisper import WhisperModel

import constants
from asr.whisper_engine import create_model, transcribe_whisper
from db.database import init_db
from db.repository import insert_transcription
import logging


logging.basicConfig(level=logging.INFO)

intents = Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

whisper_model: WhisperModel | None = None
recording_finished = asyncio.Event()


@bot.event
async def on_ready():
    global whisper_model
    
    # Ініціалізувати БД
    init_db()
    
    whisper_model = await asyncio.to_thread(
        create_model,
        model_path='models/faster-whisper-tiny',
        device='cpu',
        compute_type='int8'
    )
    logging.info("✅ Whisper model loaded")

    channel = bot.get_channel(constants.DIS_VOICE_CHANNEL_ID)

    await channel.connect()
    logging.info("🔗 Connected to voice channel %s", {channel.name})

    if (vc:= channel.guild.voice_client) and vc.is_connected():
        logging.info("🔄 Starting recording loop...")
        await record_loop(channel)


async def record_loop(channel):
    """Безперервний цикл: пишемо чанки довжиною RECORD_DURATION_SECONDS."""
    while True:
        vc = channel.guild.voice_client
        recording_finished.clear()

        vc.start_recording(WaveSink(), finished_callback)
        logging.info("🎤 Recording chunk started, talk!")

        # стільки секунд записуємо цей chunk
        await asyncio.sleep(constants.RECORD_DURATION_SECONDS)

        # тригерить finished_callback в іншому треді
        vc.stop_recording()
        logging.info("⏹️ Recording chunk stopped")
        
        # Почекати поки callback завершиться
        await recording_finished.wait()
        logging.info("✅ Callback finished, starting new cycle")


async def finished_callback(sink: WaveSink, *args):
    """Цей callback викликається в voice-треді, НЕ в async-коді."""

    for user_id, audio in sink.audio_data.items():
        # унікальне ім'я файлу (user + timestamp)
        ts = int(time.time())
        path = f"audio/temp/{user_id}_{ts}.wav"
        with open(path, "wb") as f:
            f.write(audio.file.getbuffer())

        # кинути корутину в event loop бота
        asyncio.run_coroutine_threadsafe(
            process_user_audio(user_id, path),
            bot.loop,
        )
    
    # Сигналізувати що callback завершився
    bot.loop.call_soon_threadsafe(recording_finished.set)


async def process_user_audio(user_id: int, path: str):
    whisper_text = await asyncio.to_thread(
        transcribe_whisper,
        model=whisper_model,
        path=path,
        language='ru',
    )

    word_count = whisper_text.lower().count(constants.WORD)
    
    # Зберегти в БД
    await asyncio.to_thread(
        insert_transcription,
        user_id=user_id,
        text=whisper_text,
        word_count=word_count
    )
    
    logging.info("USER %s: %s | Censored words: %s",
                 user_id,
                 whisper_text,
                 word_count)


bot.run(constants.DIS_TOKEN)
