"""
Entidades del dominio - Core de JARVIS
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class CommandType(Enum):
    """Tipos de comandos disponibles"""
    OPEN_APPLICATION = "open_application"
    SEARCH_WEB = "search_web"
    SYSTEM_CONTROL = "system_control"
    MEDIA_CONTROL = "media_control"
    INFORMATION = "information"
    GREETING = "greeting"
    EXIT = "exit"

class SentimentType(Enum):
    """Tipos de sentimientos"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class VoiceCommand:
    """Comando de voz del usuario"""
    text: str
    confidence: float
    timestamp: float
    sentiment: Optional[SentimentType] = None

@dataclass
class CommandIntent:
    """Intención del comando"""
    command_type: CommandType
    target: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    confidence: float = 0.0

@dataclass
class VoiceResponse:
    """Respuesta de voz de JARVIS"""
    text: str
    audio_data: Optional[bytes] = None
    emotion: Optional[str] = None
    priority: int = 1

@dataclass
class SystemAction:
    """Acción del sistema a ejecutar"""
    action_type: str
    target: str
    parameters: Optional[Dict[str, Any]] = None
    requires_confirmation: bool = False
