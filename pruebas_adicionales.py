# Importamos la clase Cliente del proyecto
from modelos_base import Cliente

# Importamos la excepción para datos incorrectos
from excepciones import DatoInvalidoError

# Iniciamos la prueba
print("PRUEBA: Cliente con correo incorrecto")

try:
    # Intentamos crear un cliente con un correo inválido
    cliente = Cliente(
        "CLI-PRUEBA",
        "Juan Perez",
        "correo_incorrecto",
        "3101234567"
    )

    print("PRUEBA FALLIDA: El sistema aceptó el correo.")

except DatoInvalidoError as error:
    # El programa identifica y controla el error
    print("PRUEBA EXITOSA: Correo inválido detectado.")
    print("Detalle:", error)

print("El programa continúa funcionando.")
