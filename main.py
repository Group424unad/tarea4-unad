"""
Módulo principal: main.py
Proyecto: Software FJ
Descripción general:
    Sistema integral orientado a objetos para gestionar clientes, servicios
    y reservas sin usar bases de datos.

    El sistema usa:
        - Abstracción: clases abstractas EntidadSistema y Servicio.
        - Herencia: ReservaSala, AlquilerEquipo y AsesoriaEspecializada heredan de Servicio.
        - Polimorfismo: cada servicio implementa calcular_costo() y describir() de forma diferente.
        - Encapsulación: Cliente, Servicio y Reserva protegen sus atributos internos.
        - Excepciones: errores personalizados, try/except, else, finally y encadenamiento.
        - Listas internas: clientes, servicios y reservas se guardan en listas de objetos.
        - Archivos: logs.txt guarda eventos y errores relevantes.
"""

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, Servicio
from reserva import Reserva
from excepciones import SoftwareFJError
from logger import log_event, log_error


class SistemaSoftwareFJ:
    """
    Clase administradora del sistema Software FJ.

    Esta clase mantiene las listas internas de clientes, servicios y reservas.
    No usa base de datos; todo vive en memoria durante la ejecución.
    """

    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []
        log_event("Sistema Software FJ iniciado correctamente.")

    def registrar_cliente(self, identificador: str, nombre: str, email: str, telefono: str) -> Cliente | None:
        """
        Registra un cliente en la lista interna.

        Retorna el cliente si el registro fue exitoso; retorna None si falló.
        """
        try:
            cliente = Cliente(identificador, nombre, email, telefono)
            self.clientes.append(cliente)
        except SoftwareFJError as error:
            log_error("Error controlado al registrar cliente", error)
            print(f"[ERROR CONTROLADO] Cliente no registrado: {error}")
            return None
        except Exception as error:
            log_error("Error inesperado al registrar cliente", error)
            print(f"[ERROR INESPERADO] Cliente no registrado: {error}")
            return None
        else:
            print(f"[OK] Cliente registrado: {cliente.nombre}")
            return cliente
        finally:
            log_event("Finalizó operación registrar_cliente.")

    def agregar_servicio(self, servicio: Servicio) -> bool:
        """
        Agrega un servicio ya construido a la lista interna.
        """
        try:
            if not isinstance(servicio, Servicio):
                raise TypeError("El objeto recibido no es un servicio válido.")
            self.servicios.append(servicio)
        except Exception as error:
            log_error("Error al agregar servicio", error)
            print(f"[ERROR CONTROLADO] Servicio no agregado: {error}")
            return False
        else:
            print(f"[OK] Servicio agregado: {servicio.nombre}")
            return True
        finally:
            log_event("Finalizó operación agregar_servicio.")

    def crear_reserva(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: float) -> Reserva | None:
        """
        Crea una reserva y la agrega a la lista interna.
        """
        try:
            reserva = Reserva(codigo, cliente, servicio, duracion)
            self.reservas.append(reserva)
        except SoftwareFJError as error:
            log_error("Error controlado al crear reserva", error)
            print(f"[ERROR CONTROLADO] Reserva no creada: {error}")
            return None
        except Exception as error:
            log_error("Error inesperado al crear reserva", error)
            print(f"[ERROR INESPERADO] Reserva no creada: {error}")
            return None
        else:
            print(f"[OK] Reserva creada: {reserva.codigo}")
            return reserva
        finally:
            log_event("Finalizó operación crear_reserva.")

    def mostrar_resumen(self) -> None:
        """Muestra el resumen de listas internas del sistema."""
        print("\n" + "=" * 70)
        print("RESUMEN FINAL DEL SISTEMA SOFTWARE FJ")
        print("=" * 70)
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios registrados: {len(self.servicios)}")
        print(f"Reservas registradas: {len(self.reservas)}")

        print("\nCLIENTES:")
        for cliente in self.clientes:
            print(" -", cliente.describir())

        print("\nSERVICIOS:")
        for servicio in self.servicios:
            print(" -", servicio.describir())

        print("\nRESERVAS:")
        for reserva in self.reservas:
            print(" -", reserva.describir())


def ejecutar_operacion(numero: int, descripcion: str, funcion) -> None:
    """
    Ejecuta una operación de simulación sin detener el programa ante errores.

    Parámetros:
        numero: Número de la operación simulada.
        descripcion: Texto descriptivo de la operación.
        funcion: Función anónima o bloque ejecutable.
    """
    print("\n" + "-" * 70)
    print(f"OPERACIÓN {numero}: {descripcion}")
    print("-" * 70)

    try:
        funcion()
    except SoftwareFJError as error:
        log_error(f"Operación {numero} falló con error controlado", error)
        print(f"[ERROR CONTROLADO] {error}")
    except Exception as error:
        log_error(f"Operación {numero} falló con error inesperado", error)
        print(f"[ERROR INESPERADO] {error}")
    else:
        log_event(f"Operación {numero} completada sin errores: {descripcion}")
    finally:
        # Este bloque demuestra que el sistema siempre continúa vivo.
        print(f"[INFO] Operación {numero} finalizada. El sistema continúa funcionando.")


def main() -> None:
    """Función principal que simula mínimo 10 operaciones completas."""
    sistema = SistemaSoftwareFJ()

    # Se usa un diccionario local para guardar referencias creadas durante la simulación.
    datos = {}

    ejecutar_operacion(
        1,
        "Registrar cliente válido",
        lambda: datos.update(c1=sistema.registrar_cliente("C001", "Wilmer Daza", "wilmer@email.com", "3101234567"))
    )

    ejecutar_operacion(
        2,
        "Registrar cliente inválido con email incorrecto",
        lambda: sistema.registrar_cliente("C002", "Ana Gómez", "ana-email.com", "3111234567")
    )

    ejecutar_operacion(
        3,
        "Registrar cliente inválido con teléfono no numérico",
        lambda: sistema.registrar_cliente("C003", "Carlos Pérez", "carlos@email.com", "31A123")
    )

    ejecutar_operacion(
        4,
        "Crear servicio válido de reserva de sala",
        lambda: datos.update(s1=ReservaSala("S001", "Sala Ejecutiva", 50000, capacidad=12)) or sistema.agregar_servicio(datos["s1"])
    )

    ejecutar_operacion(
        5,
        "Crear servicio válido de alquiler de equipo",
        lambda: datos.update(s2=AlquilerEquipo("S002", "Video Beam Epson", 80000, "Proyector")) or sistema.agregar_servicio(datos["s2"])
    )

    ejecutar_operacion(
        6,
        "Crear servicio válido de asesoría especializada",
        lambda: datos.update(s3=AsesoriaEspecializada("S003", "Asesoría en Python", 90000, "Programación", 4)) or sistema.agregar_servicio(datos["s3"])
    )

    ejecutar_operacion(
        7,
        "Crear servicio inválido con tarifa negativa",
        lambda: sistema.agregar_servicio(ReservaSala("S004", "Sala Defectuosa", -10000, capacidad=8))
    )

    ejecutar_operacion(
        8,
        "Crear reserva válida para sala",
        lambda: datos.update(r1=sistema.crear_reserva("R001", datos["c1"], datos["s1"], 3))
    )

    ejecutar_operacion(
        9,
        "Confirmar y procesar reserva válida con impuesto y descuento",
        lambda: (datos["r1"].confirmar(), print(f"Costo procesado: ${datos['r1'].procesar(impuesto=0.19, descuento=0.05):,.2f}"))
    )

    ejecutar_operacion(
        10,
        "Intentar cancelar una reserva ya procesada",
        lambda: datos["r1"].cancelar()
    )

    ejecutar_operacion(
        11,
        "Crear reserva fallida por duración negativa",
        lambda: sistema.crear_reserva("R002", datos["c1"], datos["s2"], -2)
    )

    ejecutar_operacion(
        12,
        "Crear reserva fallida por servicio no disponible",
        lambda: (setattr(datos["s2"], "disponible", False), sistema.crear_reserva("R003", datos["c1"], datos["s2"], 1))
    )

    ejecutar_operacion(
        13,
        "Demostrar polimorfismo listando descripción y costo base de cada servicio",
        lambda: [print(f"{servicio.describir()} | Costo 2 unidades: ${servicio.calcular_costo(2):,.2f}") for servicio in sistema.servicios]
    )

    sistema.mostrar_resumen()
    print("\nRevise el archivo logs.txt para ver eventos y errores registrados.")
    log_event("Sistema Software FJ finalizó la simulación correctamente.")


if __name__ == "__main__":
    main()
