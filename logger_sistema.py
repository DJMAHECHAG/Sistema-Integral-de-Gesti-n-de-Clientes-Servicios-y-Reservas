# Importo el módulo datetime para registrar la fecha y hora exacta de cada evento
from datetime import datetime


# Creo esta clase para administrar la escritura de eventos y errores en mi archivo de logs
class LoggerSistema:
    # Defino el constructor recibiendo el nombre del archivo donde guardaré los registros
    def __init__(self, ruta_archivo: str = "sistema_fj.log"):
        # Encapsulo la ruta del archivo de logs como atributo privado
        self.__ruta_archivo = ruta_archivo

    # Creo este método para escribir cada línea en el log controlando posibles errores de archivo
    def registrar_evento(self, nivel: str, modulo: str, mensaje: str) -> None:
        # Obtengo la marca de tiempo actual con formato legible
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Armo la línea de texto estructurada que voy a guardar
        linea_log = f"[{marca_tiempo}] [{nivel.upper()}] [{modulo}] {mensaje}\n"
        # Inicializo la variable del archivo en None antes de intentar abrirlo
        archivo = None
        # Abro un bloque try/except/finally para garantizar que el archivo siempre se cierre
        try:
            # Abro el archivo en modo 'a' (agregar al final) con codificación UTF-8
            archivo = open(self.__ruta_archivo, mode="a", encoding="utf-8")
            # Escribo la línea generada dentro del archivo
            archivo.write(linea_log)
        except OSError as error_io:
            # Si falla la escritura en disco, muestro una alerta en consola sin detener el programa
            print(f"ALERTA CRÍTICA DE LOG: No pude escribir en el archivo ({error_io})")
        finally:
            # Verifico si el archivo quedó abierto para cerrarlo de manera segura
            if archivo is not None and not archivo.closed:
                # Cierro el flujo del archivo
                archivo.close()