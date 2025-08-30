import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from application.jarvis_application import main

if __name__ == "__main__":
    main()