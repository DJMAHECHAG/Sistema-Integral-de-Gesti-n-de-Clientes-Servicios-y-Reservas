# Defino una clase base para agrupar todas mis excepciones personalizadas en Software FJ
class ErrorSistemaFJ(Exception):
    # Creo el constructor para recibir el mensaje de error y un código identificador opcional
    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        # Guardo el mensaje descriptivo del fallo
        self.mensaje = mensaje
        # Guardo el código que identifica el tipo de error
        self.codigo = codigo
        # Llamo al constructor de la clase padre Exception con el formato completo
        super().__init__(f"[{self.codigo}] {self.mensaje}")


# Creo esta excepción para lanzarla cuando los datos ingresados tengan formato o valores incorrectos
class DatoInvalidoError(ErrorSistemaFJ):
    # Defino el constructor específico para errores de validación de datos
    def __init__(self, mensaje: str):
        # Inicializo la clase padre asignando el código ERR-101
        super().__init__(mensaje, codigo="ERR-101")


# Creo esta excepción para cuando falten parámetros obligatorios en alguna operación
class ParametroFaltanteError(ErrorSistemaFJ):
    # Defino el constructor específico para ausencia de parámetros
    def __init__(self, mensaje: str):
        # Inicializo la clase padre asignando el código ERR-102
        super().__init__(mensaje, codigo="ERR-102")


# Creo esta excepción para manejar los casos en que un servicio no esté disponible
class ServicioNoDisponibleError(ErrorSistemaFJ):
    # Defino el constructor específico para indisponibilidad de servicios
    def __init__(self, mensaje: str):
        # Inicializo la clase padre asignando el código ERR-201
        super().__init__(mensaje, codigo="ERR-201")


# Creo esta excepción para controlar reservas con estados o cálculos inconsistentes
class ReservaInconsistenteError(ErrorSistemaFJ):
    # Defino el constructor específico para fallos en la gestión de reservas
    def __init__(self, mensaje: str):
        # Inicializo la clase padre asignando el código ERR-301
        super().__init__(mensaje, codigo="ERR-301")