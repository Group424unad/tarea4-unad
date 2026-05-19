"""
Módulo: servicio.py
Proyecto: Software FJ
Descripción:
    Contiene la clase abstracta Servicio y tres servicios especializados:
    ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

    Aquí se aplican herencia, polimorfismo y métodos con parámetros opcionales
    que simulan sobrecarga en Python.
"""

from abc import ABC, abstractmethod
from excepciones import ServicioInvalidoError, CalculoCostoError
from logger import log_event


class Servicio(ABC):
    """
    Clase abstracta que representa un servicio general.

    No se debe crear directamente. Sus clases hijas deben definir cómo se
    calcula el costo y cómo se describe el servicio.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True) -> None:
        self._codigo = self._validar_texto(codigo, "codigo")
        self._nombre = self._validar_texto(nombre, "nombre")
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        self._disponible = bool(disponible)
        log_event(f"Servicio creado: {self._codigo} - {self._nombre}")

    @property
    def codigo(self) -> str:
        """Devuelve el código del servicio."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        """Devuelve la tarifa base del servicio."""
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Permite cambiar la disponibilidad del servicio."""
        self._disponible = bool(estado)
        log_event(f"Disponibilidad cambiada para servicio {self._codigo}: {self._disponible}")

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        """Valida que un texto no sea vacío."""
        if not isinstance(valor, str):
            raise ServicioInvalidoError(f"El campo '{campo}' debe ser texto.")
        if not valor.strip():
            raise ServicioInvalidoError(f"El campo '{campo}' no puede estar vacío.")
        return valor.strip()

    @staticmethod
    def _validar_tarifa(tarifa: float) -> float:
        """Valida que la tarifa sea numérica y positiva."""
        if not isinstance(tarifa, (int, float)):
            raise ServicioInvalidoError("La tarifa base debe ser numérica.")
        if tarifa <= 0:
            raise ServicioInvalidoError("La tarifa base debe ser mayor que cero.")
        return float(tarifa)

    @staticmethod
    def validar_duracion(duracion: float) -> float:
        """Valida que la duración sea numérica y positiva."""
        if not isinstance(duracion, (int, float)):
            raise ServicioInvalidoError("La duración debe ser numérica.")
        if duracion <= 0:
            raise ServicioInvalidoError("La duración debe ser mayor que cero.")
        return float(duracion)

    def calcular_costo_final(self, subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Simula SOBRECARGA mediante parámetros opcionales.

        Variantes posibles:
            calcular_costo_final(subtotal)
            calcular_costo_final(subtotal, impuesto=0.19)
            calcular_costo_final(subtotal, impuesto=0.19, descuento=0.10)
        """
        try:
            if subtotal < 0:
                raise ValueError("El subtotal no puede ser negativo.")
            if not 0 <= impuesto <= 1:
                raise ValueError("El impuesto debe estar entre 0 y 1.")
            if not 0 <= descuento <= 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")

            valor_con_descuento = subtotal * (1 - descuento)
            valor_final = valor_con_descuento * (1 + impuesto)
            return round(valor_final, 2)

        except ValueError as error_original:
            # Encadenamiento de excepciones: se transforma un ValueError en una excepción del negocio.
            raise CalculoCostoError("Error al calcular el costo final del servicio.") from error_original

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Cada servicio debe implementar su propia forma de calcular el costo."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Cada servicio debe implementar su descripción."""
        pass


class ReservaSala(Servicio):
    """Servicio especializado para reservar salas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo de la sala según horas de uso."""
        duracion = self.validar_duracion(duracion)
        subtotal = self._tarifa_base * duracion
        return self.calcular_costo_final(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Descripción polimórfica del servicio de sala."""
        return f"Reserva de sala: {self._nombre} | Capacidad: {self._capacidad} personas | Tarifa/hora: {self._tarifa_base}"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquilar equipos."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._tipo_equipo = self._validar_texto(tipo_equipo, "tipo_equipo")

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo del equipo según días de alquiler."""
        duracion = self.validar_duracion(duracion)
        subtotal = self._tarifa_base * duracion
        return self.calcular_costo_final(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Descripción polimórfica del alquiler de equipo."""
        return f"Alquiler de equipo: {self._nombre} | Tipo: {self._tipo_equipo} | Tarifa/día: {self._tarifa_base}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías profesionales."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str, nivel_experto: int, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especialidad = self._validar_texto(especialidad, "especialidad")
        if not isinstance(nivel_experto, int) or not 1 <= nivel_experto <= 5:
            raise ServicioInvalidoError("El nivel experto debe ser un entero entre 1 y 5.")
        self._nivel_experto = nivel_experto

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo de asesoría.

        Se aplica un multiplicador según el nivel experto.
        """
        duracion = self.validar_duracion(duracion)
        multiplicador_experto = 1 + (self._nivel_experto * 0.10)
        subtotal = self._tarifa_base * duracion * multiplicador_experto
        return self.calcular_costo_final(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Descripción polimórfica de la asesoría."""
        return f"Asesoría especializada: {self._nombre} | Área: {self._especialidad} | Nivel: {self._nivel_experto} | Tarifa/hora: {self._tarifa_base}"
