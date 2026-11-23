
# PRUEBAS ADICIONALES - SOFTWARE FJ
# Fase 4 - Programacion UNAD

from modelos_base import Cliente
from servicios import ReservaSala
from excepciones import DatoInvalidoError

print("=" * 55)
print("PRUEBAS ADICIONALES DEL SISTEMA SOFTWARE FJ")
print("=" * 55)

# PRUEBA 1: Correo electronico incorrecto
print("\nPRUEBA 1: Correo electronico incorrecto")

try:
    cliente = Cliente(
        "CLI-PRUEBA1",
        "Juan Perez",
        "correo_incorrecto",
        "3101234567"
    )
    print("FALLIDA: Se acepto un correo incorrecto.")

except DatoInvalidoError as error:
    print("EXITOSA: El correo incorrecto fue rechazado.")
    print("Detalle:", error)


# PRUEBA 2: Nombre demasiado corto
print("\nPRUEBA 2: Nombre demasiado corto")

try:
    cliente = Cliente(
        "CLI-PRUEBA2",
        "Jo",
        "juan@gmail.com",
        "3101234567"
    )
    print("FALLIDA: Se acepto un nombre demasiado corto.")

except DatoInvalidoError as error:
    print("EXITOSA: El nombre incorrecto fue rechazado.")
    print("Detalle:", error)


# PRUEBA 3: Telefono con letras
print("\nPRUEBA 3: Telefono con letras")

try:
    cliente = Cliente(
        "CLI-PRUEBA3",
        "Maria Lopez",
        "maria@gmail.com",
        "310ABC4567"
    )
    print("FALLIDA: Se acepto un telefono incorrecto.")

except DatoInvalidoError as error:
    print("EXITOSA: El telefono incorrecto fue rechazado.")
    print("Detalle:", error)


# PRUEBA 4: Descuento superior al permitido
print("\nPRUEBA 4: Descuento superior al permitido")

try:
    sala = ReservaSala(
        "SRV-PRUEBA",
        "Sala de pruebas",
        80000,
        5
    )

    costo = sala.calcular_costo(
        2,
        descuento=0.75
    )

    print("FALLIDA: Se acepto un descuento del 75%.")

except DatoInvalidoError as error:
    print("EXITOSA: El descuento incorrecto fue rechazado.")
    print("Detalle:", error)


print("\n" + "=" * 55)
print("FINALIZARON LAS PRUEBAS ADICIONALES")
print("El programa continua funcionando.")
print("=" * 55)
