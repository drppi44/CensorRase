import logging
import time

from faster_whisper import WhisperModel

from utils import timed


# @timed
# def create_model(model_path: str, device: str, compute_type: str) -> WhisperModel:
#     return WhisperModel(
#         model_size_or_path=model_path,
#         device=device,
#         compute_type=compute_type,
#     )

# @timed
# def transcribe_whisper(model: WhisperModel, path: str, language: str) -> str:
#     segments, _ = model.transcribe(path, language=language)
#     return " ".join(seg.text for seg in segments)


def transcribe_whisper(path: str) -> str:
    t0 = time.perf_counter()
    model = WhisperModel(
        model_size_or_path='models/faster-whisper-tiny',
        device='cpu',
        # language='ru',
        compute_type='int8',
    )
    t1 = time.perf_counter()
    segments, _ = model.transcribe(path, language="ru")
    t2 = time.perf_counter()
    logging.info(f"Total time: {(t2 - t0):.2f}s")
    logging.info(f"Init model: {(t1 - t0):.2f}s")
    logging.info(f"Transcribe: {(t2 - t1):.2f}s")
    return " ".join(seg.text for seg in segments)
