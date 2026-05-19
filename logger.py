"""
Módulo: logger.py
Proyecto: Software FJ
Descripción:
    Configura el registro de eventos y errores del sistema en un archivo logs.txt.
    Este archivo funciona como evidencia de operaciones exitosas y fallidas.
"""

import logging
from pathlib import Path

# Ruta absoluta del archivo logs.txt dentro de la misma carpeta del proyecto.
LOG_FILE = Path(__file__).parent / "logs.txt"

# Configuración principal del logger.
# level=logging.INFO permite registrar información normal, advertencias y errores.
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def log_event(message: str) -> None:
    """Registra un evento informativo del sistema."""
    logging.info(message)


def log_warning(message: str) -> None:
    """Registra una advertencia del sistema."""
    logging.warning(message)


def log_error(message: str, exception: Exception | None = None) -> None:
    """
    Registra un error del sistema.

    Parámetros:
        message: Mensaje personalizado del error.
        exception: Excepción capturada, si existe.
    """
    if exception:
        logging.error(f"{message} | Tipo: {type(exception).__name__} | Detalle: {exception}")
    else:
        logging.error(message)
