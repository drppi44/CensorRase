import os
from dotenv import load_dotenv

load_dotenv()

DIS_TOKEN = os.environ["DIS_TOKEN"]
DIS_VOICE_CHANNEL_ID = int(os.environ["DIS_VOICE_CHANNEL_ID"])

WORD = os.environ["WORD"]

RECORD_DURATION_SECONDS = int(os.environ["RECORD_DURATION_SECONDS"])