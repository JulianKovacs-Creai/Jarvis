"""
Servicios del dominio - Lógica de negocio
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import VoiceCommand, CommandIntent, VoiceResponse, SystemAction, CommandType, SentimentType

class CommandProcessor(ABC):
    """Procesador de comandos - Puerto de entrada"""
    
    @abstractmethod
    def process_command(self, command: VoiceCommand) -> CommandIntent:
        """Procesa un comando de voz y retorna la intención"""
        pass

class IntentAnalyzer(ABC):
    """Analizador de intenciones - Puerto de entrada"""
    
    @abstractmethod
    def analyze_intent(self, command: VoiceCommand) -> CommandIntent:
        """Analiza la intención del comando"""
        pass

class ResponseGenerator(ABC):
    """Generador de respuestas - Puerto de salida"""
    
    @abstractmethod
    def generate_response(self, intent: CommandIntent, context: Optional[dict] = None) -> VoiceResponse:
        """Genera una respuesta basada en la intención"""
        pass

class ActionExecutor(ABC):
    """Ejecutor de acciones - Puerto de salida"""
    
    @abstractmethod
    def execute_action(self, action: SystemAction) -> bool:
        """Ejecuta una acción del sistema"""
        pass

class JarvisCore:
    """Núcleo principal de JARVIS - Orquestador"""
    
    def __init__(
        self,
        command_processor: CommandProcessor,
        intent_analyzer: IntentAnalyzer,
        response_generator: ResponseGenerator,
        action_executor: ActionExecutor
    ):
        self.command_processor = command_processor
        self.intent_analyzer = intent_analyzer
        self.response_generator = response_generator
        self.action_executor = action_executor
    
    def handle_voice_command(self, command: VoiceCommand) -> VoiceResponse:
        """Maneja un comando de voz completo"""
        # 1. Procesar comando
        intent = self.command_processor.process_command(command)
        
        # 2. Analizar intención
        analyzed_intent = self.intent_analyzer.analyze_intent(command)
        
        # 3. Generar respuesta
        response = self.response_generator.generate_response(analyzed_intent)
        
        # 4. Ejecutar acción si es necesaria
        if analyzed_intent.command_type != CommandType.GREETING:
            action = self._create_system_action(analyzed_intent)
            if action:
                self.action_executor.execute_action(action)
        
        return response
    
    def _create_system_action(self, intent: CommandIntent) -> Optional[SystemAction]:
        """Crea una acción del sistema basada en la intención"""
        if intent.command_type == CommandType.OPEN_APPLICATION:
            return SystemAction(
                action_type="open_application",
                target=intent.target or "",
                parameters=intent.parameters
            )
        elif intent.command_type == CommandType.SEARCH_WEB:
            return SystemAction(
                action_type="search_web",
                target=intent.target or "",
                parameters=intent.parameters
            )
        elif intent.command_type == CommandType.SYSTEM_CONTROL:
            return SystemAction(
                action_type="system_control",
                target=intent.target or "",
                parameters=intent.parameters
            )
        elif intent.command_type == CommandType.MEDIA_CONTROL:
            return SystemAction(
                action_type="media_control",
                target=intent.target or "",
                parameters=intent.parameters
            )
        return None
