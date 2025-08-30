"""
Adaptador de entrada - Reconocimiento de voz
"""
import speech_recognition as sr
import whisper
import tempfile
import os
from typing import Optional
from core.domain.entities import VoiceCommand, SentimentType
from core.domain.services import CommandProcessor

class WhisperSpeechRecognitionAdapter:
    """Adaptador para reconocimiento de voz usando Whisper"""
    
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ajustar para ruido ambiental
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self) -> Optional[VoiceCommand]:
        """Escucha y convierte voz a texto"""
        try:
            with self.microphone as source:
                print("🎤 Escuchando...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Usar Whisper para reconocimiento
            audio_data = audio.get_wav_data()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(audio_data)
            temp_file.close()
            
            result = self.whisper_model.transcribe(temp_file.name, language="es")
            command_text = result["text"].lower()
            
            os.unlink(temp_file.name)
            
            if command_text.strip():
                return VoiceCommand(
                    text=command_text,
                    confidence=result.get("confidence", 0.8),
                    timestamp=result.get("timestamp", 0.0)
                )
            
        except Exception as e:
            print(f"❌ Error en reconocimiento: {e}")
        
        return None

class GoogleSpeechRecognitionAdapter:
    """Adaptador para reconocimiento de voz usando Google Speech"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self) -> Optional[VoiceCommand]:
        """Escucha usando Google Speech API"""
        try:
            with self.microphone as source:
                print("🎤 Escuchando...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            command_text = self.recognizer.recognize_google(audio, language='es-ES').lower()
            
            if command_text.strip():
                return VoiceCommand(
                    text=command_text,
                    confidence=0.9,
                    timestamp=0.0
                )
            
        except Exception as e:
            print(f"❌ Error en reconocimiento: {e}")
        
        return None


