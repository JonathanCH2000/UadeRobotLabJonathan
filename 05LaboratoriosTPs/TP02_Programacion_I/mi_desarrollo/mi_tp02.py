# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Jonathan Chambi
#  Comision:           .....................................
# =====================================================================

from misiones import (
    MISION_BASICA,
    MISION_CON_ERRORES,
    MISION_CUADRADO,
    MISION_HOLA_MUNDO,
    MISION_LARGA,
)
from robot import ErrorDeSeguridad, Robot

AVANZAR = "avanzar"
GIRAR = "girar"
DETENERSE = "detenerse"
SALUDAR = "saludar"

COMANDOS_VALIDOS = (AVANZAR, GIRAR, DETENERSE, SALUDAR)
COMANDOS_QUE_LLEVAN_2_DATOS = (AVANZAR, GIRAR)
COMANDOS_QUE_LLEVAN_0_DATOS = (DETENERSE, SALUDAR)

TIPOS_DE_NUMEROS = (int, float)

VELOCIDAD_MAXIMA = 0.20
VELOCIDAD_DE_GIRO_MAXIMA = 0.50
TIEMPO_MAXIMO_POR_ORDEN = 10


def _extraer_datos_del_comando(comando):
    """Extrae los 3 comandos de la tupla y reemplaza con None los que no se encuentren presentes."""
    if not comando:
        return None, None, None

    nombre = comando[0]

    velocidad = comando[1] if len(comando) > 1 else None
    tiempo = comando[2] if len(comando) > 2 else None

    return nombre, velocidad, tiempo


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
    - que la tupla no este vacia ✅
    - que el nombre del comando sea uno de los cuatro validos ✅
    - que tenga la cantidad de datos que corresponde ✅
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
    - que velocidad y tiempo sean numeros de verdad, no textos ✅
    - que el tiempo no sea negativo ✅
    """

    # Verificamos que `comando` sea una tupla y no este vacia.
    if type(comando) is not tuple or len(comando) == 0:
        return False

    nombre, velocidad, tiempo = _extraer_datos_del_comando(comando)

    # Validamos el comando y la cantidad de sus argumentos correspondientes a cada uno.
    if nombre not in COMANDOS_VALIDOS:
        return False

    # Se necesitan 2 datos ademas del nombre del comando dentro de la tupla.
    if nombre in COMANDOS_QUE_LLEVAN_2_DATOS:
        # Solo se aceptan comandos con 3 parametros.
        if len(comando) != 3:
            return False

        # Se necesita velocidad y tiempo para estos comandos.
        if velocidad is None or tiempo is None:
            return False

        # Velocidad y tiempo deben ser enteros o flotantes.
        if (
            type(velocidad) not in TIPOS_DE_NUMEROS
            or type(tiempo) not in TIPOS_DE_NUMEROS
        ):
            return False

        # Solo se acepta tiempo positivo y debajo del maximo definido.
        if tiempo < 0 or tiempo > TIEMPO_MAXIMO_POR_ORDEN:
            return False

        # La velocidad para avanzar no debe superar el maximo definido.
        if nombre == AVANZAR and abs(velocidad) > VELOCIDAD_MAXIMA:
            return False

        # La velocidad para girar debe estar dentro del rango maximo definido.
        if nombre == GIRAR and abs(velocidad) > VELOCIDAD_DE_GIRO_MAXIMA:
            return False

    # Estos comandos no llevan ningun dato.
    if nombre in COMANDOS_QUE_LLEVAN_0_DATOS:
        if len(comando) != 1:
            return False

    # El comando es valido.
    return True


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:
        robot.avanzar(velocidad=..., tiempo=...) ✅
        robot.girar(velocidad=..., tiempo=...) ✅
        robot.detenerse() ✅
        robot.saludar() ✅

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """

    nombre, velocidad, tiempo = _extraer_datos_del_comando(comando)

    if nombre not in COMANDOS_VALIDOS:
        return "Rechazado: Comando desconocido."

    # Ejecutar el comando 'avanzar'
    if nombre == AVANZAR:
        robot.avanzar(velocidad=velocidad, tiempo=tiempo)

    # Ejecutar el comando 'girar'
    if nombre == GIRAR:
        robot.girar(velocidad=velocidad, tiempo=tiempo)

    # Ejecutar el comando 'detenerse'
    if nombre == DETENERSE:
        robot.detenerse()

    # Ejecutar el comando 'saludar'
    if nombre == SALUDAR:
        robot.saludar()

    # Todo salio bien, dar feecback de la ejecucion exitosa.
    return "Ejecutado: Comando exitoso."


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
    - si NO es valido, lo rechaza y sigue con el siguiente
    - si es valido, lo ejecuta
    - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    for comando in mision:
        try:
            if comando_es_valido(comando):
                resultado = ejecutar_comando(robot, comando)
            else:
                if type(comando) != tuple:
                    motivo = "el comando debe ser una tupla"
                elif len(comando) == 0:
                    motivo = "la tupla esta vacia"
                elif comando[0] not in ("avanzar", "girar", "detenerse", "saludar"):
                    motivo = "comando desconocido"
                elif comando[0] in ("detenerse", "saludar"):
                    motivo = "esta orden no lleva parametros"
                elif len(comando) != 3:
                    motivo = "la orden debe tener velocidad y tiempo"
                elif type(comando[1]) not in (int, float):
                    motivo = "la velocidad debe ser un numero"
                elif type(comando[2]) not in (int, float):
                    motivo = "el tiempo debe ser un numero"
                elif not 0 <= comando[2] <= 10:
                    motivo = "el tiempo debe estar entre 0 y 10 segundos"
                elif comando[0] == "avanzar":
                    motivo = "la velocidad debe estar entre -0.20 y 0.20 m/s"
                else:
                    motivo = "la velocidad de giro debe estar entre -0.50 y 0.50 rad/s"
                resultado = "Rechazado: " + motivo
        except Exception as error:
            resultado = "Rechazado: " + str(error)

        historial.append((comando, resultado))
        print(comando, "->", resultado)


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
    - cuantos comandos se ejecutaron bien
    - cuantos se rechazaron
    - cual fue el motivo de cada rechazo
    """
    ejecutados = 0
    rechazados = 0

    print("\n===== REPORTE DE LA MISION =====")
    for comando, resultado in historial:
        if resultado == "Ejecutado":
            ejecutados += 1
        else:
            rechazados += 1
            print(comando, "->", resultado)

    print("Comandos ejecutados:", ejecutados)
    print("Comandos rechazados:", rechazados)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_HOLA_MUNDO, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
