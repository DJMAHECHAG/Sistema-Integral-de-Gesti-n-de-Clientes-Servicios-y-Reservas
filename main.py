# Importo el controlador principal de mi sistema
from reservas import SistemaGestionFJ
# Importo las tres clases derivadas de Servicio
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Importo mi excepción base para capturar errores directos al instanciar servicios
from excepciones import ErrorSistemaFJ
# Importo LoggerSistema para registrar fallos en la creación directa de objetos
from logger_sistema import LoggerSistema


# Defino la función principal para ejecutar mi simulación integral de Software FJ
def ejecutar_simulacion() -> None:
    # Defino el nombre del archivo de logs
    archivo_logs = "sistema_fj.log"
    # Instancio mi sistema de gestión en memoria (sin base de datos)
    sistema = SistemaGestionFJ(archivo_logs)
    # Instancio un logger auxiliar para errores de instanciación previa
    logger_directo = LoggerSistema(archivo_logs)

    # Imprimo el encabezado de inicio de mi simulación
    print("=" * 75)
    print("INICIANDO SIMULACIÓN DEL SISTEMA INTEGRAL - SOFTWARE FJ")
    print("=" * 75)

    # --- BLOQUE 1: GESTIÓN DE CLIENTES (VÁLIDOS E INVÁLIDOS) ---
    print("\n--- FASE 1: REGISTRO DE CLIENTES ---")

    # Operación 1 (Válida): Registro correctamente un cliente corporativo
    cliente_1 = sistema.registrar_cliente("CLI-001", "Laura Gómez", "laura.gomez@empresa.com", "3104567890")

    # Operación 2 (Válida): Registro correctamente un segundo cliente
    cliente_2 = sistema.registrar_cliente("CLI-002", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")

    # Operación 3 (Inválida): Pruebo un correo sin dominio válido para disparar DatoInvalidoError
    sistema.registrar_cliente("CLI-003", "Andrés Ruiz", "andres_sin_arroba.com", "3112223344")

    # Operación 4 (Inválida): Pruebo teléfono con letras e ID duplicado para disparar DatoInvalidoError
    sistema.registrar_cliente("CLI-001", "Laura Duplicada", "otra@correo.com", "300ABC")

    # --- BLOQUE 2: CREACIÓN DE SERVICIOS (VÁLIDOS E INVÁLIDOS) ---
    print("\n--- FASE 2: REGISTRO DE SERVICIOS ESPECIALIZADOS ---")

    # Operación 5 (Válida): Creo y registro una Sala de Juntas
    sala_juntas = sistema.registrar_servicio(
        ReservaSala("SRV-01", "Sala Innovación A", tarifa_base=80000.0, capacidad=10, tiene_proyector=True)
    )

    # Operación 6 (Válida): Creo y registro un Alquiler de Equipos
    equipos_dev = sistema.registrar_servicio(
        AlquilerEquipo("SRV-02", "Workstations RTX", tarifa_base=35000.0, tipo_equipo="Portátil Desarrollo", cantidad_unidades=3)
    )

    # Operación 7 (Válida): Creo y registro una Asesoría Especializada
    asesoria_arq = sistema.registrar_servicio(
        AsesoriaEspecializada("SRV-03", "Auditoría Arquitectura Cloud", tarifa_base=120000.0, especialidad="Cloud & DevOps", modalidad="Presencial")
    )

    # Operación 8 (Inválida): Intento crear una sala con tarifa negativa para disparar DatoInvalidoError
    try:
        # Intento instanciar un servicio con tarifa negativa
        sala_invalida = ReservaSala("SRV-04", "Sala Defectuosa", tarifa_base=-50000.0, capacidad=5)
        # Intento registrarla si llegara a crearse
        sistema.registrar_servicio(sala_invalida)
    except ErrorSistemaFJ as error:
        # Registro el fallo en mi archivo de logs y continúo la ejecución
        logger_directo.registrar_evento("ERROR", "Servicios", f"Error al instanciar servicio: {error}")
        print(f"[ERROR CONTROLADO - CREACIÓN SERVICIO] {error}")

    # --- BLOQUE 3: GESTIÓN DE RESERVAS (EXITOSAS Y FALLIDAS) ---
    print("\n--- FASE 3: PROCESAMIENTO Y CONFIRMACIÓN DE RESERVAS ---")

    # Operación 9 (Exitosa): Reservo la sala por 4 horas con 10% de descuento (sobrecarga opcional)
    reserva_1 = sistema.crear_y_confirmar_reserva("RES-101", cliente_1, sala_juntas, duracion_horas=4, descuento=0.10)

    # Operación 10 (Fallida - Servicio no disponible): Intento reservar la misma sala ya ocupada
    sistema.crear_y_confirmar_reserva("RES-102", cliente_2, sala_juntas, duracion_horas=2)

  
    # --- BLOQUE 4: PRUEBAS ADICIONALES DE RESERVAS ---
    print("\n--- FASE 4: VALIDACIONES Y CANCELACIONES ---")

    # Operación 11 (Fallida): Intento reservar equipos por 1 hora.
    # El servicio exige una duración mínima de 2 horas.
    reserva_11 = sistema.crear_y_confirmar_reserva(
        "RES-103",
        cliente_1,
        equipos_dev,
        duracion_horas=1
    )

    # Compruebo que el sistema rechazó la duración inválida.
    if reserva_11 is None:
        print("[PRUEBA 11 OK] Se rechazó la duración inválida.")
    else:
        print("[PRUEBA 11 FALLIDA] Se aceptó una duración inválida.")

    # Operación 12: Creo una asesoría de 3 horas con 5 % de descuento.
    reserva_12 = sistema.crear_y_confirmar_reserva(
        "RES-104",
        cliente_2,
        asesoria_arq,
        duracion_horas=3,
        descuento=0.05
    )

    # Compruebo que se creó y confirmó la reserva.
    if reserva_12 is not None and reserva_12.estado == "CONFIRMADA":
        print("[PRUEBA 12 OK] Asesoría confirmada correctamente.")
    else:
        print("[PRUEBA 12 FALLIDA] No se confirmó la asesoría.")

    # Cancelo la reserva de sala creada en la operación 9.
    if reserva_1 is not None:
        sistema.cancelar_reserva(reserva_1)

        # Compruebo que la cancelación fue correcta.
        if reserva_1.estado == "CANCELADA":
            print("[OK] Primera cancelación realizada.")
        else:
            print("[ERROR] No se canceló correctamente.")

        # Intento cancelarla nuevamente.
        # El sistema debe controlar ReservaInconsistenteError.
        sistema.cancelar_reserva(reserva_1)

        # Compruebo que el programa continúa funcionando.
        print("[PRUEBA FINAL] El programa sigue funcionando.")
    else:
        print("[ERROR] La reserva inicial no está disponible.")


    # Imprimo el mensaje final confirmando que completé todas las pruebas sin interrupciones
    print("\n" + "=" * 75)
    print("SIMULACIÓN FINALIZADA EXITOSAMENTE SIN CAÍDAS DEL SISTEMA.")
    print(f"Revise el archivo '{archivo_logs}' para auditar todos los eventos y errores.")
    print("=" * 75)


# Defino el punto de entrada estándar de Python
if __name__ == "__main__":
    # Ejecuto mi simulación principal
    ejecutar_simulacion()
