"""
Adaptador de salida - Acciones del sistema
"""
import subprocess
import webbrowser
# import pyautogui
import os
from typing import Dict, Any, Optional
from core.domain.entities import SystemAction
from core.domain.services import ActionExecutor

class SystemActionAdapter(ActionExecutor):
    """Adaptador para ejecutar acciones del sistema"""
    
    def __init__(self):
        self.application_mapping = {
            "calculadora": "calc",
            "notepad": "notepad",
            "bloc de notas": "notepad",
            "explorador": "explorer",
            "chrome": "chrome",
            "spotify": "spotify",
            "discord": "discord",
            "steam": "steam"
        }
    
    def execute_action(self, action: SystemAction) -> bool:
        """Ejecuta una acción del sistema"""
        try:
            if action.action_type == "open_application":
                return self._open_application(action.target)
            elif action.action_type == "search_web":
                return self._search_web(action.target)
            elif action.action_type == "system_control":
                return self._system_control(action.target, action.parameters)
            elif action.action_type == "media_control":
                return self._media_control(action.target)
            else:
                print(f"Acción no reconocida: {action.action_type}")
                return False
                
        except Exception as e:
            print(f"Error ejecutando acción: {e}")
            return False
    
    def _open_application(self, target: str) -> bool:
        """Abre una aplicación"""
        app_name = self.application_mapping.get(target.lower(), target)
        try:
            subprocess.Popen(app_name)
            return True
        except Exception as e:
            print(f"Error abriendo {app_name}: {e}")
            return False
    
    def _search_web(self, query: str) -> bool:
        """Busca en la web"""
        try:
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            return True
        except Exception as e:
            print(f"Error en búsqueda web: {e}")
            return False
    
    def _system_control(self, action: str, parameters: Optional[Dict[str, Any]] = None) -> bool:
        """Control del sistema (versión WSL2)"""
        try:
            if "volumen" in action:
                print(f" Control de volumen: {action}")
                # En WSL2 solo mostrar mensaje
            elif "apagar" in action:
                print(" Comando de apagado (no ejecutado en WSL2)")
            elif "reiniciar" in action:
                print("🔄 Comando de reinicio (no ejecutado en WSL2)")
            
            return True
        except Exception as e:
            print(f"Error en control del sistema: {e}")
            return False
    
    def _media_control(self, action: str) -> bool:
        """Control de medios (versión WSL2)"""
        try:
            print(f" Control de medios: {action}")
            # En WSL2 solo mostrar mensaje
            return True
        except Exception as e:
            print(f"Error en control de medios: {e}")
            return False