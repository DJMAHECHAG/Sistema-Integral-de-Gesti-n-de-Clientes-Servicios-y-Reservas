# Importo abstractmethod para declarar los métodos polimórficos obligatorios
from abc import abstractmethod
# Importo EntidadSistema desde mi módulo modelos_base
from modelos_base import EntidadSistema
# Importo mis excepciones para validar parámetros y disponibilidad
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


# Creo la clase abstracta Servicio heredando de EntidadSistema
class Servicio(EntidadSistema):
    # Defino el constructor común para todos los servicios de Software FJ
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        # Inicializo el ID usando la clase padre EntidadSistema
        super().__init__(id_servicio)
        # Valido que el nombre del servicio no esté vacío
        if not nombre_servicio or not isinstance(nombre_servicio, str):
            # Lanzo excepción si el nombre viene vacío
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        # Valido que la tarifa base sea un número positivo mayor a cero
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            # Lanzo excepción si la tarifa es cero o negativa
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor a 0.")
        # Encapsulo el nombre del servicio
        self.__nombre_servicio = nombre_servicio.strip()
        # Encapsulo la tarifa base como flotante
        self.__tarifa_base = float(tarifa_base)
        # Encapsulo el estado de disponibilidad
        self.__disponible = bool(disponible)

    # Defino propiedad de lectura para el nombre del servicio
    @property
    def nombre_servicio(self) -> str:
        # Retorno el nombre del servicio
        return self.__nombre_servicio

    # Defino propiedad de lectura para la tarifa base
    @property
    def tarifa_base(self) -> float:
        # Retorno el valor numérico de la tarifa base
        return self.__tarifa_base

    # Defino propiedad de lectura para consultar si el servicio está disponible
    @property
    def disponible(self) -> bool:
        # Retorno True si está disponible o False si está ocupado
        return self.__disponible

    # Creo este método para actualizar la disponibilidad del servicio
    def cambiar_disponibilidad(self, estado: bool) -> None:
        # Actualizo el atributo privado disponible
        self.__disponible = bool(estado)

    # Declaro el método abstracto polimórfico para validar los parámetros de cada servicio
    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        # Obligo a que cada subclase implemente su propia validación
        pass

    # Declaro el método abstracto polimórfico con sobrecarga opcional (descuentos e impuestos)
    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Obligo a que cada subclase implemente su cálculo de costo
        pass

    # Declaro el método abstracto polimórfico para describir cada servicio
    @abstractmethod
    def describir_servicio(self) -> str:
        # Obligo a que cada subclase retorne su descripción
        pass

    # Implemento obtener_resumen llamando a describir_servicio
    def obtener_resumen(self) -> str:
        # Retorno la descripción completa del servicio
        return self.describir_servicio()

    # Creo este método auxiliar protegido para aplicar descuentos e impuestos (sobrecarga funcional)
    def _aplicar_ajustes_financieros(self, subtotal: float, descuento: float, impuesto: float) -> float:
        # Valido que el descuento esté entre 0% y 50%
        if not (0.0 <= descuento <= 0.5):
            # Lanzo excepción si el descuento está fuera del rango permitido
            raise DatoInvalidoError("El descuento debe estar entre 0% (0.0) y 50% (0.5).")
        # Valido que el porcentaje de impuesto no sea negativo
        if impuesto < 0.0:
            # Lanzo excepción si el impuesto es negativo
            raise DatoInvalidoError("El porcentaje de impuesto no puede ser negativo.")
        # Calculo el valor después de restar el descuento
        con_descuento = subtotal * (1.0 - descuento)
        # Calculo el valor final sumando el impuesto (por defecto IVA 19%)
        total = con_descuento * (1.0 + impuesto)
        # Retorno el total redondeado a 2 decimales
        return round(total, 2)


# Creo la subclase 1: Servicio especializado para Reserva de Salas
class ReservaSala(Servicio):
    # Defino el constructor añadiendo capacidad de personas y si incluye proyector
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, capacidad: int, tiene_proyector: bool = True):
        # Llamo al constructor de la clase Servicio
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        # Valido que la capacidad de la sala sea mínimo de 2 personas
        if not isinstance(capacidad, int) or capacidad < 2:
            # Lanzo excepción si la capacidad es menor a 2
            raise DatoInvalidoError("La capacidad de la sala debe ser de al menos 2 personas.")
        # Encapsulo la capacidad
        self.__capacidad = capacidad
        # Encapsulo si tiene proyector
        self.__tiene_proyector = bool(tiene_proyector)

    # Sobrescribo la validación: las salas se reservan entre 1 y 12 horas
    def validar_parametros(self, duracion_horas: int) -> None:
        # Verifico primero que la sala esté disponible
        if not self.disponible:
            # Lanzo excepción si la sala ya está reservada
            raise ServicioNoDisponibleError(f"La sala '{self.nombre_servicio}' no está disponible.")
        # Verifico que la duración sea un entero entre 1 y 12 horas
        if not isinstance(duracion_horas, int) or not (1 <= duracion_horas <= 12):
            # Lanzo excepción si las horas salen del rango permitido
            raise DatoInvalidoError("La reserva de sala debe durar entre 1 y 12 horas.")

    # Sobrescribo el cálculo de costo sumando un recargo fijo si incluye proyector
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Ejecuto primero la validación de parámetros
        self.validar_parametros(duracion_horas)
        # Sumo 15000 de recargo si la sala tiene proyector
        recargo_proyector = 15000.0 if self.__tiene_proyector else 0.0
        # Calculo el subtotal multiplicando la tarifa por las horas y sumando el recargo
        subtotal = (self.tarifa_base * duracion_horas) + recargo_proyector
        # Retorno el total aplicando descuentos e impuestos
        return self._aplicar_ajustes_financieros(subtotal, descuento, impuesto)

    # Sobrescribo la descripción detallada de la sala
    def describir_servicio(self) -> str:
        # Defino el texto según tenga o no proyector
        texto_proyector = "con proyector" if self.__tiene_proyector else "sin proyector"
        # Retorno la descripción formateada de la sala
        return f"Sala '{self.nombre_servicio}' (Capacidad: {self.__capacidad} pers., {texto_proyector}) - Tarifa: ${self.tarifa_base}/h"


# Creo la subclase 2: Servicio especializado para Alquiler de Equipos
class AlquilerEquipo(Servicio):
    # Defino el constructor añadiendo el tipo de equipo y la cantidad de unidades
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, tipo_equipo: str, cantidad_unidades: int = 1):
        # Llamo al constructor de Servicio
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        # Valido que el tipo de equipo no esté vacío
        if not tipo_equipo or not isinstance(tipo_equipo, str):
            # Lanzo excepción si no se indica el tipo de equipo
            raise DatoInvalidoError("Debe especificar el tipo de equipo a alquilar.")
        # Valido que la cantidad de unidades sea mínimo 1
        if not isinstance(cantidad_unidades, int) or cantidad_unidades < 1:
            # Lanzo excepción si la cantidad es menor a 1
            raise DatoInvalidoError("La cantidad de equipos debe ser al menos 1.")
        # Encapsulo el tipo de equipo
        self.__tipo_equipo = tipo_equipo.strip()
        # Encapsulo la cantidad de unidades
        self.__cantidad_unidades = cantidad_unidades

    # Sobrescribo la validación: el alquiler de equipos requiere mínimo 2 horas
    def validar_parametros(self, duracion_horas: int) -> None:
        # Verifico que los equipos estén disponibles
        if not self.disponible:
            # Lanzo excepción si no hay disponibilidad
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre_servicio}' no está disponible.")
        # Valido que la duración sea entera y de al menos 2 horas
        if not isinstance(duracion_horas, int) or duracion_horas < 2:
            # Lanzo excepción si piden menos de 2 horas
            raise DatoInvalidoError("El alquiler de equipos requiere un mínimo de 2 horas.")

    # Sobrescribo el cálculo de costo multiplicando tarifa, horas y cantidad de equipos
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Ejecuto la validación de parámetros
        self.validar_parametros(duracion_horas)
        # Calculo el subtotal multiplicando tarifa base, duración y unidades
        subtotal = self.tarifa_base * duracion_horas * self.__cantidad_unidades
        # Aplico descuentos e impuestos y retorno el total
        return self._aplicar_ajustes_financieros(subtotal, descuento, impuesto)

    # Sobrescribo la descripción del alquiler de equipos
    def describir_servicio(self) -> str:
        # Retorno la descripción formateada del equipo
        return f"Alquiler Equipo '{self.nombre_servicio}' ({self.__tipo_equipo} x{self.__cantidad_unidades}) - Tarifa: ${self.tarifa_base}/h"


# Creo la subclase 3: Servicio especializado para Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    # Defino el constructor añadiendo especialidad técnica y modalidad (Virtual o Presencial)
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, especialidad: str, modalidad: str = "Virtual"):
        # Llamo al constructor de Servicio
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        # Valido que la especialidad no esté vacía
        if not especialidad or not isinstance(especialidad, str):
            # Lanzo excepción si falta la especialidad
            raise DatoInvalidoError("La especialidad de la asesoría es obligatoria.")
        # Valido que la modalidad sea Virtual o Presencial
        if modalidad not in ("Virtual", "Presencial"):
            # Lanzo excepción si escriben una modalidad distinta
            raise DatoInvalidoError("La modalidad debe ser 'Virtual' o 'Presencial'.")
        # Encapsulo especialidad y modalidad
        self.__especialidad = especialidad.strip()
        self.__modalidad = modalidad

    # Sobrescribo la validación: las asesorías duran entre 1 y 8 horas
    def validar_parametros(self, duracion_horas: int) -> None:
        # Verifico disponibilidad del consultor
        if not self.disponible:
            # Lanzo excepción si no hay agenda disponible
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre_servicio}' no tiene agenda disponible.")
        # Valido que las horas estén entre 1 y 8
        if not isinstance(duracion_horas, int) or not (1 <= duracion_horas <= 8):
            # Lanzo excepción si la duración está fuera de rango
            raise DatoInvalidoError("Las asesorías deben durar entre 1 y 8 horas.")

    # Sobrescribo el cálculo de costo aplicando un 10% extra si la asesoría es Presencial
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Ejecuto la validación de parámetros
        self.validar_parametros(duracion_horas)
        # Calculo el costo base por horas
        subtotal = self.tarifa_base * duracion_horas
        # Si es Presencial, sumo un 10% adicional por desplazamiento
        if self.__modalidad == "Presencial":
            subtotal *= 1.10
        # Aplico descuentos e impuestos y retorno el valor final
        return self._aplicar_ajustes_financieros(subtotal, descuento, impuesto)

    # Sobrescribo la descripción de la asesoría
    def describir_servicio(self) -> str:
        # Retorno la descripción formateada de la asesoría
        return f"Asesoría '{self.nombre_servicio}' [Área: {self.__especialidad} | {self.__modalidad}] - Tarifa: ${self.tarifa_base}/h"