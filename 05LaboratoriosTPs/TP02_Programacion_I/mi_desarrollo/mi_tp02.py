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
    - que velocidad y tiempo sean numeros de verdad, no textos
    - que el tiempo no sea negativo
    """

    # Verificamos que `comando` sea una tupla y no este vacia.
    if type(comando) is not tuple or len(comando) == 0:
        return False

    nombre, velocidad, tiempo = _extraer_datos_del_comando(comando)

    # Validamos el comando y la cantidad de sus argumentos correspondientes a cada uno.
    if nombre not in COMANDOS_VALIDOS:
        return False

    if nombre in COMANDOS_QUE_LLEVAN_2_DATOS:
        if velocidad is None:
            return False

    if nombre in COMANDOS_QUE_LLEVAN_0_DATOS:
        if velocidad is not None or tiempo is not None:
            return False

    match comando[0]:
        case "avanzar" | "girar":
            if len(comando) != 3:
                return False
            velocidad = comando[1]
            tiempo = comando[2]
            if type(velocidad) not in (int, float):
                return False
            if type(tiempo) not in (int, float):
                return False
            if not 0 <= tiempo <= 10:
                return False
            if comando[0] == "avanzar":
                return -0.20 <= velocidad <= 0.20
            return -0.50 <= velocidad <= 0.50
        case "detenerse" | "saludar":
            return len(comando) == 1
        case _:
            return False


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    try:
        match comando[0]:
            case "avanzar":
                robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            case "girar":
                robot.girar(velocidad=comando[1], tiempo=comando[2])
            case "detenerse":
                robot.detenerse()
            case "saludar":
                robot.saludar()
            case _:
                return "Rechazado: comando desconocido"
        return "Ejecutado"
    except ErrorDeSeguridad as error:
        return "Rechazado: " + str(error)


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
