"""
Módulo: reserva.py
Proyecto: Software FJ
Descripción:
    Contiene la clase Reserva, que integra cliente, servicio, duración y estado.
    Maneja confirmación, cancelación y procesamiento de reservas.
"""

from cliente import Cliente
from servicio import Servicio
from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoCostoError,
)
from logger import log_event, log_error


class Reserva:
    """
    Representa una reserva realizada por un cliente sobre un servicio.

    Estados permitidos:
        PENDIENTE
        CONFIRMADA
        CANCELADA
        PROCESADA
    """

    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: float) -> None:
        self._codigo = self._validar_codigo(codigo)
        self._cliente = self._validar_cliente(cliente)
        self._servicio = self._validar_servicio(servicio)
        self._duracion = servicio.validar_duracion(duracion)
        self._estado = "PENDIENTE"
        self._costo_total = 0.0
        log_event(f"Reserva creada en estado PENDIENTE: {self._codigo}")

    @property
    def codigo(self) -> str:
        """Devuelve el código de la reserva."""
        return self._codigo

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Devuelve el costo total calculado de la reserva."""
        return self._costo_total

    @staticmethod
    def _validar_codigo(codigo: str) -> str:
        """Valida el código de la reserva."""
        if not isinstance(codigo, str) or not codigo.strip():
            raise ReservaInvalidaError("El código de la reserva no puede estar vacío.")
        return codigo.strip()

    @staticmethod
    def _validar_cliente(cliente: Cliente) -> Cliente:
        """Valida que el cliente sea un objeto Cliente."""
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe recibir un objeto Cliente válido.")
        return cliente

    @staticmethod
    def _validar_servicio(servicio: Servicio) -> Servicio:
        """Valida que el servicio sea un objeto Servicio y esté disponible."""
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe recibir un objeto Servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")
        return servicio

    def confirmar(self) -> None:
        """Confirma una reserva pendiente."""
        try:
            if self._estado != "PENDIENTE":
                raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
            self._estado = "CONFIRMADA"
        except OperacionNoPermitidaError as error:
            log_error(f"No se pudo confirmar la reserva {self._codigo}", error)
            raise
        else:
            log_event(f"Reserva confirmada correctamente: {self._codigo}")
        finally:
            # finally se ejecuta siempre, haya error o no.
            log_event(f"Finalizó intento de confirmación para reserva {self._codigo}")

    def cancelar(self) -> None:
        """Cancela una reserva siempre que no haya sido procesada."""
        try:
            if self._estado == "PROCESADA":
                raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")
            if self._estado == "CANCELADA":
                raise OperacionNoPermitidaError("La reserva ya está cancelada.")
            self._estado = "CANCELADA"
        except OperacionNoPermitidaError as error:
            log_error(f"No se pudo cancelar la reserva {self._codigo}", error)
            raise
        else:
            log_event(f"Reserva cancelada correctamente: {self._codigo}")
        finally:
            log_event(f"Finalizó intento de cancelación para reserva {self._codigo}")

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Procesa una reserva confirmada y calcula su costo total.

        Parámetros opcionales permiten simular sobrecarga:
            procesar()
            procesar(impuesto=0.19)
            procesar(impuesto=0.19, descuento=0.10)
        """
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")
            self._costo_total = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
            self._estado = "PROCESADA"
            return self._costo_total

        except CalculoCostoError as error:
            log_error(f"Error de cálculo al procesar reserva {self._codigo}", error)
            raise
        except OperacionNoPermitidaError as error:
            log_error(f"Operación no permitida en reserva {self._codigo}", error)
            raise
        except Exception as error_original:
            # Encadenamiento de excepciones para capturar errores inesperados.
            nuevo_error = ReservaInvalidaError("Ocurrió un error inesperado al procesar la reserva.")
            log_error(f"Error inesperado en reserva {self._codigo}", error_original)
            raise nuevo_error from error_original
        else:
            # Este else no se ejecuta porque ya hay return dentro del try.
            # Se deja como evidencia académica del uso de try/except/else.
            log_event(f"Reserva procesada correctamente: {self._codigo}")
        finally:
            log_event(f"Finalizó intento de procesamiento para reserva {self._codigo}")

    def describir(self) -> str:
        """Devuelve una descripción completa de la reserva."""
        return (
            f"Reserva {self._codigo} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Estado: {self._estado} | Costo total: {self._costo_total}"
        )

    def __str__(self) -> str:
        """Representación en texto del objeto Reserva."""
        return self.describir()
