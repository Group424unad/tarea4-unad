"""
Módulo: excepciones.py
Proyecto: Software FJ
Descripción:
    Este archivo contiene excepciones personalizadas para controlar errores
    del sistema sin detener la ejecución general del programa.
"""


class SoftwareFJError(Exception):
    """Clase base para todas las excepciones personalizadas del sistema."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato recibido no cumple las validaciones requeridas."""
    pass


class ClienteInvalidoError(DatosInvalidosError):
    """Se lanza cuando los datos de un cliente son incorrectos."""
    pass


class ServicioInvalidoError(DatosInvalidosError):
    """Se lanza cuando los datos de un servicio son incorrectos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse correctamente."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando el estado actual no permite ejecutar una operación."""
    pass


class CalculoCostoError(SoftwareFJError):
    """Se lanza cuando ocurre un error en el cálculo del costo de un servicio."""
    pass
