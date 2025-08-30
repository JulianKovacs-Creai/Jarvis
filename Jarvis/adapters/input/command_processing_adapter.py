"""
Adaptador de entrada - Procesamiento de comandos
"""
import re
from typing import Dict, Any
from core.domain.entities import VoiceCommand, CommandIntent, CommandType
from core.domain.services import CommandProcessor, IntentAnalyzer

class AICommandProcessorAdapter(CommandProcessor):
    """Adaptador para procesamiento de comandos con IA"""
    
    def __init__(self):
        self.command_patterns = {
            CommandType.OPEN_APPLICATION: [
                r"abrir\s+(\w+)",
                r"iniciar\s+(\w+)",
                r"ejecutar\s+(\w+)",
                r"lanzar\s+(\w+)"
            ],
            CommandType.SEARCH_WEB: [
                r"buscar\s+(.+)",
                r"encontrar\s+(.+)",
                r"investigar\s+(.+)"
            ],
            CommandType.SYSTEM_CONTROL: [
                r"(subir|bajar)\s+volumen",
                r"silenciar",
                r"(apagar|reiniciar)\s+computadora"
            ],
            CommandType.MEDIA_CONTROL: [
                r"(pausar|reproducir|siguiente|anterior)",
                r"(play|pause|next|previous)"
            ],
            CommandType.INFORMATION: [
                r"qué\s+hora\s+es",
                r"qué\s+fecha\s+es",
                r"información\s+del\s+sistema"
            ],
            CommandType.GREETING: [
                r"hola\s+jarvis",
                r"hey\s+jarvis",
                r"buenos\s+(días|tardes|noches)"
            ],
            CommandType.EXIT: [
                r"adiós",
                r"hasta\s+luego",
                r"salir",
                r"terminar"
            ]
        }
    
    def process_command(self, command: VoiceCommand) -> CommandIntent:
        """Procesa un comando usando patrones de IA"""
        text = command.text.lower()
        
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    target = match.group(1) if match.groups() else None
                    return CommandIntent(
                        command_type=command_type,
                        target=target,
                        confidence=command.confidence
                    )
        
        # Comando no reconocido
        return CommandIntent(
            command_type=CommandType.GREETING,
            confidence=0.0
        )

class IntentAnalyzerAdapter(IntentAnalyzer):
    """Adaptador para análisis de intenciones con IA"""
    
    def __init__(self):
        self.sentiment_keywords = {
            "positive": ["gracias", "excelente", "perfecto", "genial"],
            "negative": ["error", "problema", "mal", "terrible"],
            "neutral": ["ok", "bien", "normal"]
        }
    
    def analyze_intent(self, command: VoiceCommand) -> CommandIntent:
        """Analiza la intención del comando"""
        # Análisis básico de sentimientos
        sentiment = self._analyze_sentiment(command.text)
        
        # Crear intención
        intent = CommandIntent(
            command_type=self._determine_command_type(command.text),
            confidence=command.confidence
        )
        
        return intent
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analiza el sentimiento del texto"""
        text_lower = text.lower()
        
        for sentiment, keywords in self.sentiment_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return sentiment
        
        return "neutral"
    
    def _determine_command_type(self, text: str) -> CommandType:
        """Determina el tipo de comando"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["abrir", "iniciar", "ejecutar"]):
            return CommandType.OPEN_APPLICATION
        elif any(word in text_lower for word in ["buscar", "encontrar"]):
            return CommandType.SEARCH_WEB
        elif any(word in text_lower for word in ["volumen", "silenciar"]):
            return CommandType.SYSTEM_CONTROL
        elif any(word in text_lower for word in ["pausar", "reproducir", "siguiente"]):
            return CommandType.MEDIA_CONTROL
        elif any(word in text_lower for word in ["hora", "fecha"]):
            return CommandType.INFORMATION
        elif any(word in text_lower for word in ["adiós", "salir"]):
            return CommandType.EXIT
        else:
            return CommandType.GREETING
