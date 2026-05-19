"""
Módulo: cliente.py
Proyecto: Software FJ
Descripción:
    Contiene la clase abstracta EntidadSistema y la clase Cliente.
    Aquí se aplica abstracción y encapsulación.
"""

from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError
from logger import log_event


class EntidadSistema(ABC):
    """
    Clase abstracta general para representar entidades del sistema.

    Esta clase demuestra ABSTRACCIÓN porque define una estructura común,
    pero no se usa directamente para crear objetos.
    """

    def __init__(self, identificador: str) -> None:
        self._identificador = self._validar_texto(identificador, "identificador")

    @property
    def identificador(self) -> str:
        """Permite leer el identificador de forma controlada."""
        return self._identificador

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        """
        Valida que un campo de texto no esté vacío.

        Este método se usa internamente para evitar repetir código.
        """
        if not isinstance(valor, str):
            raise ClienteInvalidoError(f"El campo '{campo}' debe ser texto.")
        if not valor.strip():
            raise ClienteInvalidoError(f"El campo '{campo}' no puede estar vacío.")
        return valor.strip()

    @abstractmethod
    def describir(self) -> str:
        """Método abstracto que cada entidad debe implementar."""
        pass


class Cliente(EntidadSistema):
    """
    Representa un cliente de Software FJ.

    Esta clase aplica ENCAPSULACIÓN porque sus datos personales se guardan
    en atributos protegidos y se validan mediante setters y métodos privados.
    """

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str) -> None:
        super().__init__(identificador)
        self._nombre = self._validar_nombre(nombre)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)
        log_event(f"Cliente registrado correctamente: {self._identificador} - {self._nombre}")

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del cliente."""
        return self._nombre

    @property
    def email(self) -> str:
        """Devuelve el correo del cliente."""
        return self._email

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        """Permite cambiar el nombre después de validarlo."""
        self._nombre = self._validar_nombre(nuevo_nombre)
        log_event(f"Nombre actualizado para cliente {self._identificador}")

    @email.setter
    def email(self, nuevo_email: str) -> None:
        """Permite cambiar el email después de validarlo."""
        self._email = self._validar_email(nuevo_email)
        log_event(f"Email actualizado para cliente {self._identificador}")

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        """Permite cambiar el teléfono después de validarlo."""
        self._telefono = self._validar_telefono(nuevo_telefono)
        log_event(f"Teléfono actualizado para cliente {self._identificador}")

    def _validar_nombre(self, nombre: str) -> str:
        """Valida que el nombre tenga mínimo tres caracteres."""
        nombre = self._validar_texto(nombre, "nombre")
        if len(nombre) < 3:
            raise ClienteInvalidoError("El nombre debe tener mínimo 3 caracteres.")
        return nombre.title()

    def _validar_email(self, email: str) -> str:
        """Valida formato básico de correo electrónico."""
        email = self._validar_texto(email, "email").lower()
        if "@" not in email or "." not in email:
            raise ClienteInvalidoError("El email debe contener '@' y un dominio válido.")
        return email

    def _validar_telefono(self, telefono: str) -> str:
        """Valida que el teléfono contenga solo números y tenga mínimo 7 dígitos."""
        telefono = self._validar_texto(telefono, "telefono")
        if not telefono.isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números.")
        if len(telefono) < 7:
            raise ClienteInvalidoError("El teléfono debe tener mínimo 7 dígitos.")
        return telefono

    def describir(self) -> str:
        """Devuelve una descripción legible del cliente."""
        return f"Cliente: {self._nombre} | Email: {self._email} | Teléfono: {self._telefono}"

    def __str__(self) -> str:
        """Representación en texto del objeto Cliente."""
        return self.describir()
