# ------------ PUBLIC EXPORTS ------------
# Importamos las funciones principales desde el módulo 'main'
from .main import requirements, importer, installer

# ------------ METADATA ------------
__title__ = "pyimporter"
__version__ = "1.0.0"
__author__ = "Ander Emiliano Santos Ponce / Espartan113"
__description__ = "Instalador e importador dinámico de dependencias para Python."

# Definimos exactamente qué se exporta si alguien hace `from tu_paquete import *`
__all__ = [
    "requirements",
    "importer",
    "installer",
]