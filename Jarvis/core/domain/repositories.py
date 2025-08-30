"""
Repositorios del dominio - Persistencia de datos
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import VoiceCommand, CommandIntent

class CommandRepository(ABC):
    """Repositorio de comandos - Puerto de salida"""
    
    @abstractmethod
    def save_command(self, command: VoiceCommand) -> bool:
        """Guarda un comando"""
        pass
    
    @abstractmethod
    def get_recent_commands(self, limit: int = 10) -> List[VoiceCommand]:
        """Obtiene comandos recientes"""
        pass

class IntentRepository(ABC):
    """Repositorio de intenciones - Puerto de salida"""
    
    @abstractmethod
    def save_intent(self, intent: CommandIntent) -> bool:
        """Guarda una intención"""
        pass
    
    @abstractmethod
    def get_intent_history(self, limit: int = 10) -> List[CommandIntent]:
        """Obtiene historial de intenciones"""
        pass
