"""
Aplicación principal de JARVIS usando Arquitectura Hexagonal
"""
import time
from typing import Optional
from core.domain.entities import VoiceCommand, VoiceResponse
from core.domain.services import JarvisCore
from adapters.input.speech_recognition_adapter import WhisperSpeechRecognitionAdapter
from adapters.input.command_processing_adapter import AICommandProcessorAdapter, IntentAnalyzerAdapter
from adapters.output.voice_synthesis_adapter import VibeVoiceSynthesisAdapter, CoquiTTSSynthesisAdapter
from adapters.output.system_action_adapter import SystemActionAdapter

class JarvisApplication:
    """Aplicación principal de JARVIS"""
    
    def __init__(self):
        print("🤖 Inicializando JARVIS con Arquitectura Hexagonal...")
        
        # Configurar adaptadores
        self._setup_adapters()
        
        # Configurar núcleo
        self._setup_core()
        
        # Configuración de la aplicación
        self.is_running = True
        self.wake_word = "jarvis"
        
        print("✅ JARVIS inicializado correctamente")
    
    def _setup_adapters(self):
        """Configura los adaptadores de entrada y salida"""
        # Adaptadores de entrada
        self.speech_recognition = WhisperSpeechRecognitionAdapter()
        self.command_processor = AICommandProcessorAdapter()
        self.intent_analyzer = IntentAnalyzerAdapter()
        
        # Adaptadores de salida
        self.voice_synthesis = VibeVoiceSynthesisAdapter()
        self.system_action = SystemActionAdapter()
        
        # Fallback para síntesis de voz
        if not hasattr(self.voice_synthesis, 'use_vibevoice') or not self.voice_synthesis.use_vibevoice:
            self.voice_synthesis = CoquiTTSSynthesisAdapter()
    
    def _setup_core(self):
        """Configura el núcleo de JARVIS"""
        self.core = JarvisCore(
            command_processor=self.command_processor,
            intent_analyzer=self.intent_analyzer,
            response_generator=self.voice_synthesis,
            action_executor=self.system_action
        )
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Mensaje de bienvenida
        welcome_response = VoiceResponse(text="JARVIS está activo y listo para ayudarte")
        self.voice_synthesis.speak(welcome_response)
        
        print("�� JARVIS está escuchando...")
        print("💡 Di 'Jarvis' seguido de tu comando")
        print("🔴 Di 'adiós' para salir")
        
        while self.is_running:
            # Escuchar comando
            command = self.speech_recognition.listen()
            
            if command:
                # Verificar palabra de activación
                if self.wake_word in command.text.lower():
                    # Procesar comando
                    response = self.core.handle_voice_command(command)
                    
                    # Reproducir respuesta
                    self.voice_synthesis.speak(response)
                    
                    # Verificar si es comando de salida
                    if "adiós" in command.text.lower() or "salir" in command.text.lower():
                        self.is_running = False
                
                elif any(word in command.text.lower() for word in ["hola jarvis", "hey jarvis"]):
                    # Saludo directo
                    greeting_response = VoiceResponse(text="Hola, ¿en qué puedo ayudarte?")
                    self.voice_synthesis.speak(greeting_response)
        
        # Mensaje de despedida
        goodbye_response = VoiceResponse(text="JARVIS se está cerrando. Hasta luego!")
        self.voice_synthesis.speak(goodbye_response)
        print("👋 JARVIS se ha cerrado")

def main():
    """Función principal"""
    try:
        jarvis = JarvisApplication()
        jarvis.run()
    except KeyboardInterrupt:
        print("\n👋 JARVIS interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error en JARVIS: {e}")

if __name__ == "__main__":
    main()