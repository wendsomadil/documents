# core/multimedia/audio/speech_to_text.py
from google.cloud import speech_v1p1beta1 as speech
from config.settings import settings
import io

class SpeechToText:
    def __init__(self):
        self.client = speech.SpeechClient()
        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="fr-FR",  # Français prioritaire
            alternative_language_codes=["en-US"],  # Anglais en fallback
            enable_automatic_punctuation=True,
            model="latest_long",  # Modèle optimisé pour audio long
        )
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcrit un fichier audio en texte
        
        Args:
            audio_file_path: Chemin vers le fichier audio (WAV, MP3, etc.)
            
        Returns:
            Texte transcrit
        """
        try:
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            
            # Transcription synchrone (fichiers < 1 minute)
            response = self.client.recognize(config=self.config, audio=audio)
            
            # Extraction du meilleur résultat
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return transcript.strip()
        
        except Exception as e:
            print(f"❌ Erreur transcription : {e}")
            return ""
    
    async def transcribe_long_audio(self, audio_file_path: str) -> str:
        """Transcription asynchrone pour fichiers > 1 minute"""
        # Upload vers Google Cloud Storage puis long_running_recognize()
        pass