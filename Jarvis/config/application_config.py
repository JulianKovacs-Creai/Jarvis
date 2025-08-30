"""
Configuración de la aplicación JARVIS
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SpeechConfig:
    """Configuración de reconocimiento de voz"""
    wake_word: str = "jarvis"
    language: str = "es-ES"
    timeout: int = 5
    phrase_time_limit: int = 5
    use_whisper: bool = True
    whisper_model: str = "base"

@dataclass
class VoiceConfig:
    """Configuración de síntesis de voz"""
    use_vibevoice: bool = True
    fallback_to_coqui: bool = True
    voice_rate: int = 150
    voice_volume: float = 0.9

@dataclass
class SystemConfig:
    """Configuración del sistema"""
    applications: Dict[str, str] = None
    web_search_engine: str = "https://www.google.com/search?q={}"
    require_confirmation: bool = False

@dataclass
class JarvisConfig:
    """Configuración principal de JARVIS"""
    speech: SpeechConfig = None
    voice: VoiceConfig = None
    system: SystemConfig = None
    
    def __post_init__(self):
        if self.speech is None:
            self.speech = SpeechConfig()
        if self.voice is None:
            self.voice = VoiceConfig()
        if self.system is None:
            self.system = SystemConfig(
                applications={
                    "calculadora": "calc",
                    "notepad": "notepad",
                    "explorador": "explorer",
                    "chrome": "chrome",
                    "spotify": "spotify"
                }
            )

# Configuración por defecto
DEFAULT_CONFIG = JarvisConfig()