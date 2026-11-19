# Importo ABC y abstractmethod para construir mis clases y métodos abstractos
from abc import ABC, abstractmethod
# Importo mis excepciones personalizadas para validar los atributos
from excepciones import DatoInvalidoError, ParametroFaltanteError


# Defino la clase abstracta base que representa cualquier entidad dentro de Software FJ
class EntidadSistema(ABC):
    # Creo el constructor base para asignar un identificador único a cada entidad
    def __init__(self, id_entidad: str):
        # Valido que el identificador no sea nulo ni una cadena vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            # Lanzo mi excepción si el ID viene vacío o inválido
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        # Encapsulo el ID limpio como atributo privado
        self.__id_entidad = id_entidad.strip()

    # Defino una propiedad de solo lectura para consultar el ID de la entidad
    @property
    def id_entidad(self) -> str:
        # Retorno el valor del identificador encapsulado
        return self.__id_entidad

    # Defino el método abstracto que obligará a las clases hijas a mostrar su resumen
    @abstractmethod
    def obtener_resumen(self) -> str:
        # Dejo el método sin implementación en la clase base abstracta
        pass


# Creo la clase Cliente heredando de EntidadSistema con encapsulación y validaciones
class Cliente(EntidadSistema):
    # Defino el constructor para inicializar documento, nombre, correo y teléfono
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llamo al constructor de mi clase abstracta padre
        super().__init__(id_cliente)
        # Asigno los atributos a través de los setters para que pasen por las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # Defino el getter para leer el nombre del cliente
    @property
    def nombre(self) -> str:
        # Retorno el atributo privado nombre
        return self.__nombre

    # Defino el setter para validar y guardar el nombre del cliente
    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Verifico que sea una cadena de texto con al menos 3 caracteres válidos
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            # Lanzo DatoInvalidoError si el nombre es muy corto o inválido
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        # Guardo el nombre limpio en el atributo privado
        self.__nombre = valor.strip()

    # Defino el getter para leer el correo electrónico del cliente
    @property
    def correo(self) -> str:
        # Retorno el atributo privado correo
        return self.__correo

    # Defino el setter para validar y guardar el correo electrónico
    @correo.setter
    def correo(self, valor: str) -> None:
        # Verifico que el correo tenga '@' y un punto en el dominio
        if not valor or not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            # Lanzo DatoInvalidoError si el formato del correo no es válido
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        # Guardo el correo en minúsculas y sin espacios extra
        self.__correo = valor.strip().lower()

    # Defino el getter para leer el teléfono del cliente
    @property
    def telefono(self) -> str:
        # Retorno el atributo privado teléfono
        return self.__telefono

    # Defino el setter para validar y guardar el número de teléfono
    @telefono.setter
    def telefono(self, valor: str) -> None:
        # Verifico que el teléfono tenga solo dígitos y entre 7 y 15 números
        if not valor or not isinstance(valor, str) or not valor.strip().isdigit() or not (7 <= len(valor.strip()) <= 15):
            # Lanzo DatoInvalidoError si el teléfono tiene letras o longitud incorrecta
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos.")
        # Guardo el teléfono limpio en el atributo privado
        self.__telefono = valor.strip()

    # Implemento el método abstracto obtener_resumen para esta clase
    def obtener_resumen(self) -> str:
        # Retorno una cadena formateada con los datos encapsulados del cliente
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"