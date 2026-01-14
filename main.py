import time

from discord import Intents
from discord import sinks
from discord.ext import commands
from discord.sinks import WaveSink
import asyncio

from faster_whisper import WhisperModel

import constants
# from asr.whisper_engine import create_model
from asr.whisper_engine import transcribe_whisper
import logging


logging.basicConfig(level=logging.INFO)


intents = Intents.default()
intents.voice_states = True
# intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

whisper_model: WhisperModel | None = None

# Лічильник для кожного юзера
# user_counter = {}

async def record_loop(vc):
    """Безперервний цикл: пишемо чанки довжиною RECORD_DURATION_SECONDS."""
    while True:
        sink = WaveSink()
        vc.start_recording(sink, finished_callback)
        await asyncio.sleep(0.5)  # Дати час Discord API запустити запис
        logging.info("🎤 Recording chunk started, talk!")

        # стільки секунд записуємо цей chunk
        await asyncio.sleep(constants.RECORD_DURATION_SECONDS)

        # тригерить finished_callback в іншому треді
        # і одразу цикл продовжиться, стартуючи новий sink
        vc.stop_recording()
        logging.info("⏹️ Recording chunk stopped")


@bot.event
async def on_ready():
    # global whisper_model
    # whisper_model = await asyncio.to_thread(
    #     create_model,
    #     model_path='models/faster-whisper-tiny',
    #     device='cpu',
    #     compute_type='int8'
    # )

    logging.debug('✅ Getting the channel from config')
    channel = bot.get_channel(constants.DIS_VOICE_CHANNEL_ID)
    logging.debug('✅ On_ready: channel %s', channel.name)

    await channel.connect()
    logging.info("🔗 Connected to voice channel %s", {channel.name})

    await asyncio.sleep(3)  # Дати Discord підʼєднатися  # TODO обовьязково чекати?
    vc = channel.guild.voice_client
    logging.debug('✅ Voice client %s' ,vc)

    if vc and vc.is_connected():
        # bot.loop.create_task(record_loop(vc))
        logging.info("🔄 Starting recording loop...")
        await record_loop(vc)



# TODO: check tiny and base models. they are cpu less required as small one clocks async loop -> tiny the best
# TODO: user_id.waw недостатньо, тре ще час враховувати для унікальності. можуть перетертися записи
# TODO: записи повині постійно створюватись і відправлятись на перевірку. система не повина пропускати слова


async def finished_callback(sink: sinks, *args):
    """Цей callback викликається в voice-треді, НЕ в async-коді."""
    logging.debug('✅ finished_callback has been called!')

    for user_id, audio in sink.audio_data.items():
        # унікальне ім'я файлу (user + timestamp)
        ts = int(time.time())
        path = f"audio/temp/{user_id}_{ts}.wav"
        with open(path, "wb") as f:
            f.write(audio.file.getbuffer())

        # кинути корутину в event loop бота
        # asyncio.run_coroutine_threadsafe(
        #     process_user_audio(user_id, path),
        #     bot.loop,
        # )

    # при бажанні почистити sink
    # sink.cleanup()


# async def process_user_audio(user_id: int, path: str):
#     whisper_text = await asyncio.to_thread(
#         transcribe_whisper,
#         model=whisper_model,
#         path=path,
#         language='ru',
#     )
#
#     logging.info(f"USER {user_id}")
#     logging.info("WHISPER: %s", whisper_text)
#
#     cnt_whisper = whisper_text.lower().count(constants.WORD)
#     logging.info('Censored words: %s', cnt_whisper)



bot.run(constants.DIS_TOKEN)
