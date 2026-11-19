# Importo EntidadSistema y Cliente desde mi módulo modelos_base
from modelos_base import EntidadSistema, Cliente
# Importo Servicio desde mi módulo servicios
from servicios import Servicio
# Importo LoggerSistema para registrar eventos y fallos
from logger_sistema import LoggerSistema
# Importo mis excepciones personalizadas
from excepciones import (
    ErrorSistemaFJ,
    DatoInvalidoError,
    ServicioNoDisponibleError,
    ReservaInconsistenteError,
)


# Creo la clase Reserva para integrar Cliente, Servicio, duración y estado
class Reserva(EntidadSistema):
    # Defino el constructor que inicia la reserva en estado PENDIENTE
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        # Inicializo el identificador único mediante la clase padre
        super().__init__(id_reserva)
        # Valido que el cliente recibido sea una instancia de Cliente
        if not isinstance(cliente, Cliente):
            # Lanzo DatoInvalidoError si no es un objeto Cliente
            raise DatoInvalidoError("La reserva requiere un objeto Cliente válido.")
        # Valido que el servicio recibido sea una instancia de Servicio
        if not isinstance(servicio, Servicio):
            # Lanzo DatoInvalidoError si no es un objeto Servicio
            raise DatoInvalidoError("La reserva requiere un objeto Servicio válido.")
        # Encapsulo cliente y servicio
        self.__cliente = cliente
        self.__servicio = servicio
        # Ejecuto la validación de parámetros del servicio para las horas solicitadas
        self.__servicio.validar_parametros(duracion_horas)
        # Encapsulo la duración en horas
        self.__duracion_horas = duracion_horas
        # Inicio el estado en PENDIENTE
        self.__estado = "PENDIENTE"
        # Inicio el costo total en 0.0 hasta procesar el cálculo
        self.__costo_total = 0.0

    # Defino propiedades de lectura para consultar los atributos encapsulados
    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    # Creo este método para calcular el costo de la reserva aplicando encadenamiento de excepciones
    def procesar_reserva(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Abro un bloque try para capturar errores matemáticos o de validación
        try:
            # Verifico que la reserva no esté cancelada
            if self.__estado == "CANCELADA":
                # Lanzo excepción si intentan procesar una reserva cancelada
                raise ReservaInconsistenteError("No se puede procesar una reserva que ya fue cancelada.")
            # Calculo el costo llamando polimórficamente al método del servicio
            costo_calculado = self.__servicio.calcular_costo(self.__duracion_horas, descuento, impuesto)
            # Verifico que el cálculo no dé un valor nulo o negativo
            if costo_calculado <= 0:
                # Lanzo ValueError interno para encadenarlo después
                raise ValueError("El cálculo arrojó un monto total nulo o negativo.")
            # Guardo el costo calculado
            self.__costo_total = costo_calculado
            # Cambio el estado a PROCESADA
            self.__estado = "PROCESADA"
            # Retorno el costo total
            return self.__costo_total
        except (DatoInvalidoError, ServicioNoDisponibleError, ValueError) as err_origen:
            # Encadeno la excepción original dentro de ReservaInconsistenteError usando 'from'
            raise ReservaInconsistenteError(
                f"Fallo al procesar la reserva {self.id_entidad}: {err_origen}"
            ) from err_origen

    # Creo este método para confirmar una reserva ya procesada
    def confirmar_reserva(self) -> None:
        # Verifico que la reserva esté en estado PROCESADA antes de confirmarla
        if self.__estado != "PROCESADA":
            # Lanzo excepción si intentan confirmar sin haber procesado
            raise ReservaInconsistenteError(
                f"No se puede confirmar la reserva {self.id_entidad} en estado '{self.__estado}'."
            )
        # Cambio el estado a CONFIRMADA
        self.__estado = "CONFIRMADA"
        # Marco el servicio como ocupado (no disponible)
        self.__servicio.cambiar_disponibilidad(False)

    # Creo este método para cancelar una reserva y liberar el servicio
    def cancelar_reserva(self) -> None:
        # Verifico que no esté ya cancelada
        if self.__estado == "CANCELADA":
            # Lanzo excepción si intentan cancelar dos veces
            raise ReservaInconsistenteError(f"La reserva {self.id_entidad} ya se encuentra cancelada.")
        # Si estaba confirmada, vuelvo a habilitar la disponibilidad del servicio
        if self.__estado == "CONFIRMADA":
            # Restauro la disponibilidad del servicio
            self.__servicio.cambiar_disponibilidad(True)
        # Cambio el estado a CANCELADA
        self.__estado = "CANCELADA"

    # Implemento el método abstracto obtener_resumen
    def obtener_resumen(self) -> str:
        # Retorno los datos consolidados de la reserva
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre_servicio} | "
            f"Duración: {self.__duracion_horas}h | Total: ${self.__costo_total:,.2f}"
        )


# Creo la clase controladora que gestiona listas en memoria (sin base de datos) y control global de errores
class SistemaGestionFJ:
    # Defino el constructor inicializando mis listas internas y el sistema de logs
    def __init__(self, archivo_log: str = "sistema_fj.log"):
        # Creo la lista en memoria para guardar objetos Cliente
        self.__clientes: list[Cliente] = []
        # Creo la lista en memoria para guardar objetos Servicio
        self.__servicios: list[Servicio] = []
        # Creo la lista en memoria para guardar objetos Reserva
        self.__reservas: list[Reserva] = []
        # Instancio mi clase LoggerSistema
        self.__logger = LoggerSistema(archivo_log)

    # Creo este método para registrar clientes usando try/except/else
    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Cliente | None:
        # Abro bloque try para intentar crear y validar el cliente
        try:
            # Verifico que no exista otro cliente con el mismo ID
            if any(c.id_entidad == id_cliente for c in self.__clientes):
                # Lanzo excepción por ID duplicado
                raise DatoInvalidoError(f"Ya existe un cliente registrado con ID '{id_cliente}'.")
            # Instancio el nuevo cliente (ejecuta validaciones internas)
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as error:
            # Registro el error en mi archivo de logs sin detener la ejecución
            self.__logger.registrar_evento("ERROR", "Clientes", str(error))
            # Muestro el error controlado en consola
            print(f"[ERROR CONTROLADO - CLIENTE] {error}")
            # Retorno None indicando que falló el registro
            return None
        else:
            # En el bloque else agrego el cliente solo si no hubo excepciones
            self.__clientes.append(nuevo_cliente)
            # Registro el éxito en el log
            self.__logger.registrar_evento("INFO", "Clientes", f"Cliente creado: {nuevo_cliente.obtener_resumen()}")
            # Imprimo confirmación en consola
            print(f"[OK - CLIENTE] {nuevo_cliente.obtener_resumen()}")
            # Retorno el cliente creado
            return nuevo_cliente

    # Creo este método para registrar servicios usando try/except/else
    def registrar_servicio(self, servicio: Servicio) -> Servicio | None:
        # Abro bloque try para validar y guardar el servicio en mi lista interna
        try:
            # Verifico que sea una instancia válida de Servicio
            if not isinstance(servicio, Servicio):
                # Lanzo excepción si pasan otro tipo de objeto
                raise DatoInvalidoError("El objeto proporcionado no es un Servicio válido.")
            # Verifico que el ID del servicio no esté repetido
            if any(s.id_entidad == servicio.id_entidad for s in self.__servicios):
                # Lanzo excepción por ID duplicado
                raise DatoInvalidoError(f"El ID de servicio '{servicio.id_entidad}' ya existe.")
        except ErrorSistemaFJ as error:
            # Guardo el fallo en el archivo de logs
            self.__logger.registrar_evento("ERROR", "Servicios", str(error))
            # Muestro el error controlado en consola
            print(f"[ERROR CONTROLADO - SERVICIO] {error}")
            # Retorno None
            return None
        else:
            # Si no hubo errores, guardo el servicio en la lista en memoria
            self.__servicios.append(servicio)
            # Registro el evento en el log
            self.__logger.registrar_evento("INFO", "Servicios", f"Servicio registrado: {servicio.describir_servicio()}")
            # Imprimo confirmación
            print(f"[OK - SERVICIO] {servicio.describir_servicio()}")
            # Retorno el servicio registrado
            return servicio

    # Creo este método para crear, procesar y confirmar reservas usando try/except/else/finally
    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.19,
    ) -> Reserva | None:
        # Declaro una variable auxiliar para la reserva
        reserva_actual = None
        # Abro el bloque try principal para ejecutar toda la transacción
        try:
            # Instancio la reserva (valida cliente, servicio y duración)
            reserva_actual = Reserva(id_reserva, cliente, servicio, duracion_horas)
            # Proceso el cálculo financiero con descuentos e impuestos
            reserva_actual.procesar_reserva(descuento=descuento, impuesto=impuesto)
            # Confirmo la reserva y bloqueo disponibilidad del servicio
            reserva_actual.confirmar_reserva()
        except ErrorSistemaFJ as error:
            # Capturo cualquier excepción personalizada o encadenada
            causa = f" | Causa original: {error.__cause__}" if error.__cause__ else ""
            # Registro el fallo detallado en el log
            self.__logger.registrar_evento("ERROR", "Reservas", f"{error}{causa}")
            # Muestro el error en consola sin detener el sistema
            print(f"[ERROR CONTROLADO - RESERVA] {error}{causa}")
            # Retorno None
            return None
        else:
            # Si todo salió bien, guardo la reserva en mi lista en memoria
            self.__reservas.append(reserva_actual)
            # Registro la confirmación exitosa en el log
            self.__logger.registrar_evento("INFO", "Reservas", f"Reserva confirmada: {reserva_actual.obtener_resumen()}")
            # Muestro confirmación en consola
            print(f"[OK - RESERVA] {reserva_actual.obtener_resumen()}")
            # Retorno la reserva confirmada
            return reserva_actual
        finally:
            # Uso el bloque finally para dejar siempre una traza de auditoría del intento
            self.__logger.registrar_evento("AUDIT", "Reservas", f"Finalizado intento de operación para reserva '{id_reserva}'.")

    # =========================================================================
    # TODO (PARA OTRO INTEGRANTE): Completar el método cancelar_reserva
    # =========================================================================
    def cancelar_reserva(self, reserva: Reserva) -> None:
        # TODO: Implementar un bloque try/except que valide si 'reserva' es una instancia de Reserva,
        # llame a reserva.cancelar_reserva(), registre el éxito o el error (ErrorSistemaFJ) en self.__logger
        # e imprima el mensaje correspondiente en consola sin detener el programa.
        pass