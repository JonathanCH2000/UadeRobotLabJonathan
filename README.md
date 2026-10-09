# TP02 - Programación I: Controlador de misiones

**Integrantes:** CHAMBI HUACA JONATHAN AGUSTIN, COSENTINI RODRIGO, PEÑA CAMILA ISABEL, PUEGHER NICOLAS ALEJANDRO

## Descripción

Programa que recorre una misión (lista de comandos) para un robot.

1. **Valida** cada comando (`comando_es_valido`).
2. **Ejecuta** cada comando en el robot (`ejecutar_comando`), atrapando `ErrorDeSeguridad`.
3. **Recorre** la misión completa sin cortarse por comandos inválidos (`ejecutar_mision`).
4. **Reporta** cuántos comandos se ejecutaron, cuántos se rechazaron y por qué (`generar_reporte`).

## Modalidad de desarrollo

Mixta (principalmente manual, con asistencia de IA para mejorar la impresión de los reportes de las partes 3 y 4).

## Tiempo empleado (en minutos)

| Actividad                      | Jonathan | Nicolás |   Total |
| ------------------------------ | -------: | ------: | ------: |
| Análisis                       |       21 |      45 |      66 |
| Programación                   |       57 |     120 |     177 |
| Pruebas                        |       28 |      60 |      88 |
| Presentación (incluye reporte) |       14 |      30 |      44 |
| **Total**                      |  **120** | **255** | **375** |

## Uso de IA

| Dato                 | Detalle                 |
| -------------------- | ----------------------- |
| Herramienta          | Claude (modalidad chat) |
| Modelo               | Claude Haiku 5.5        |
| Thinking effort      | Medio                   |
| Tokens empleados     | Desconozco              |
| Estimación del gasto | Desconozco              |

### Para qué se usó

- Proponer mejoras de formato para los `print` de las partes 3 y 4 (títulos, numeración de pasos y contadores alineados).
- Chequear errores ortográficos en el `README.md`.
