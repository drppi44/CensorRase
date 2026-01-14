from faster_whisper import WhisperModel


def create_model(model_path: str, device: str, compute_type: str) -> WhisperModel:
    return WhisperModel(
        model_size_or_path=model_path,
        device=device,
        compute_type=compute_type,
    )


def transcribe_whisper(model: WhisperModel, path: str, language: str = 'ru') -> str:
    segments, _ = model.transcribe(path, language=language)
    return " ".join(seg.text for seg in segments)
