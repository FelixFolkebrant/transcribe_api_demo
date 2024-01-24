from fastapi import UploadFile
from pydub import AudioSegment
from io import BytesIO
import logging


async def pre_process_audio(
    upload_file: UploadFile,
    sample_rate: int,
    new_file_path="processed_audio.wav",
):
    """Processes the uploaded audio file to meet the requirements of the STT engine.
    1. Convert to mono
    2. Set sample rate to specified sample rate
    """
    try:
        # Read the audio file asynchronously
        file_bytes = await upload_file.read()
        audio = AudioSegment.from_file(
            BytesIO(file_bytes), format=upload_file.filename.split(".")[-1]
        )
        audio = audio.set_frame_rate(sample_rate).set_channels(1)
        audio.export(new_file_path, format="wav")
        return new_file_path
    except Exception as e:
        logging.error(f"Error processing audio file: {e}")
        return None