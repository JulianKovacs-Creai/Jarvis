"""
Adaptador de salida - Síntesis de voz
"""
import torch
import numpy as np
from scipy.io import wavfile
import tempfile
import pygame
import os
from typing import Optional
from core.domain.entities import VoiceResponse
from core.domain.services import ResponseGenerator

class VibeVoiceSynthesisAdapter(ResponseGenerator):
    """Adaptador para síntesis de voz usando VibeVoice"""
    
    def __init__(self):
        try:
            from vibevoice import VibeVoice
            self.vibevoice = VibeVoice.from_pretrained("microsoft/speecht5_tts")
            self.vibevoice.eval()
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.vibevoice.to(self.device)
            self.use_vibevoice = True
            pygame.mixer.init()
            print("✅ VibeVoice configurado")
        except Exception as e:
            print(f"❌ Error configurando VibeVoice: {e}")
            self.use_vibevoice = False
    
    def generate_response(self, intent, context: Optional[dict] = None) -> VoiceResponse:
        """Genera respuesta de voz usando VibeVoice"""
        response_text = self._generate_response_text(intent, context)
        
        if self.use_vibevoice:
            audio_data = self._synthesize_speech(response_text)
            return VoiceResponse(
                text=response_text,
                audio_data=audio_data
            )
        else:
            return VoiceResponse(text=response_text)
    
    def _generate_response_text(self, intent, context: Optional[dict] = None) -> str:
        """Genera el texto de respuesta"""
        responses = {
            "open_application": "Abriendo {target}",
            "search_web": "Buscando {target}",
            "system_control": "Ejecutando comando de sistema",
            "media_control": "Control de medios ejecutado",
            "information": "Aquí tienes la información",
            "greeting": "Hola, ¿en qué puedo ayudarte?",
            "exit": "Hasta luego, que tengas un buen día"
        }
        
        response_template = responses.get(intent.command_type.value, "Comando ejecutado")
        return response_template.format(target=intent.target or "aplicación")
    
    def _synthesize_speech(self, text: str) -> Optional[bytes]:
        """Sintetiza voz usando VibeVoice"""
        try:
            with torch.no_grad():
                audio = self.vibevoice.generate_speech(text, self.device)
            
            audio_np = audio.cpu().numpy()
            audio_np = audio_np / np.max(np.abs(audio_np))
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            wavfile.write(temp_file.name, 22050, audio_np)
            
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_file.name)
            return audio_data
            
        except Exception as e:
            print(f"Error en síntesis: {e}")
            return None
    
    def speak(self, response: VoiceResponse):
        """Reproduce la respuesta de voz"""
        if response.audio_data and self.use_vibevoice:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(response.audio_data)
            temp_file.close()
            
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            os.unlink(temp_file.name)
        else:
            print(f"JARVIS: {response.text}")

class CoquiTTSSynthesisAdapter(ResponseGenerator):
    """Adaptador para síntesis de voz usando Coqui TTS"""
    
    def __init__(self):
        try:
            from TTS.api import TTS
            self.tts = TTS("tts_models/es/css10/vits")
            self.use_coqui = True
            pygame.mixer.init()
            print("✅ Coqui TTS configurado")
        except Exception as e:
            print(f"❌ Error configurando Coqui TTS: {e}")
            self.use_coqui = False
    
    def generate_response(self, intent, context: Optional[dict] = None) -> VoiceResponse:
        """Genera respuesta usando Coqui TTS"""
        response_text = self._generate_response_text(intent, context)
        
        if self.use_coqui:
            audio_data = self._synthesize_speech(response_text)
            return VoiceResponse(
                text=response_text,
                audio_data=audio_data
            )
        else:
            return VoiceResponse(text=response_text)
    
    def _generate_response_text(self, intent, context: Optional[dict] = None) -> str:
        """Genera el texto de respuesta"""
        # Similar al VibeVoice adapter
        responses = {
            "open_application": "Abriendo {target}",
            "search_web": "Buscando {target}",
            "system_control": "Ejecutando comando de sistema",
            "media_control": "Control de medios ejecutado",
            "information": "Aquí tienes la información",
            "greeting": "Hola, ¿en qué puedo ayudarte?",
            "exit": "Hasta luego, que tengas un buen día"
        }
        
        response_template = responses.get(intent.command_type.value, "Comando ejecutado")
        return response_template.format(target=intent.target or "aplicación")
    
    def _synthesize_speech(self, text: str) -> Optional[bytes]:
        """Sintetiza voz usando Coqui TTS"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            self.tts.tts_to_file(text=text, file_path=temp_file.name)
            
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_file.name)
            return audio_data
            
        except Exception as e:
            print(f"Error en síntesis: {e}")
            return None
    
    def speak(self, response: VoiceResponse):
        """Reproduce la respuesta de voz"""
        if response.audio_data and self.use_coqui:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(response.audio_data)
            temp_file.close()
            
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            os.unlink(temp_file.name)
        else:
            print(f"JARVIS: {response.text}")

