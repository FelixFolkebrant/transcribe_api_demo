import logging
import os
from abc import ABC, abstractmethod

from fastapi import UploadFile
from google.cloud import speech
from utils.pre_processor import pre_process_audio

# Configure logging
logging.basicConfig(level=logging.INFO)

CREDENTIALS_PATH = "../credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH


class STTModel(ABC):
    """Abstract base class for Speech-To-Text models forcing a transcribe"""

    @abstractmethod
    def transcribe(self, audio_file):
        pass


class GoogleSTTStrategy(STTModel):
    """STT model using Google's speech-to-text service."""
    # ! Currently synchronous which needs to be fixed

    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe(self, audio_file):
        try:
            with open(audio_file, "rb") as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16_000,
                language_code="sv-SE",
                enable_automatic_punctuation=True,
            )

            response = self.client.recognize(config=config, audio=audio)
            result = ""
            for result in response.results:
                logging.info(f"Transcript: {result.alternatives[0].transcript}")
                logging.info(f"Confidence: {result.alternatives[0].confidence}")
            return response.results[0].alternatives[0].transcript
        except Exception as e:
            logging.error(f"Error during transcription: {e}")


class Transcriber:
    """Handles the transcription process using the specified STT model."""

    def __init__(self, model: STTModel):
        self.model = model

    async def transcribe(self, upload_file: UploadFile):
        """Transcribes the given uploaded audio file using the configured STT model."""
        processed_file_path = await pre_process_audio(upload_file, 16_000)
        if processed_file_path:
            transcription = self.model.transcribe(processed_file_path)
            return transcription
