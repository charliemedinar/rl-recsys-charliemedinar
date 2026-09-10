"""Reto de la sesion 3 · Escriba usted la recompensa.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

El agente de la cuadricula tarda mucho en encontrar la meta porque durante
cientos de episodios no recibe ninguna senal util: solo el coste de cada paso.
Su trabajo es **darle una pista**, escribiendo una recompensa extra.

Rellene ``mi_moldeado``. Recibe tres cosas y devuelve un numero, que se suma a
la recompensa que el entorno ya entrega.

    anterior   la casilla donde estaba, como (fila, columna). Puede ser None
               en el primer paso.
    siguiente  la casilla a la que acaba de llegar.
    terminal   True si ``siguiente`` termina el episodio.

No hay ninguna restriccion sobre lo que puede escribir. Puede usar la
distancia a la meta, la fila, la columna, lo que se le ocurra.

═══════════════════════════════════════════════════════════════════════════
COMO SE SABE SI FUNCIONO
═══════════════════════════════════════════════════════════════════════════

    uv run python scripts/reto3.py        entrena y mide, e imprime el veredicto
    uv run pytest tests/test_reto3.py     comprueba el contrato

**Antes de ejecutar nada, escriba su prediccion en la bitacora.** Que espera
que haga su agente. Cuantos pasos va a tardar. Que retorno va a sacar.

Aviso, y va en serio: es muy probable que su primera version obtenga un
retorno estupendo y sea un desastre. Cuando eso pase, no lo arregle todavia.
Anotelo, que de eso trata la clase.
"""

from __future__ import annotations

# Estas dos las puede mover libremente.
GAMMA = 0.9      # tiene que ser el mismo descuento con el que se entrena
ESCALA = 0.5     # cuanto pesa su pista frente al coste del paso, que es -0,04

PENALIZACION = 1.5   # cuanto mas pesa alejarse que lo que se gana al acercarse

META = (0, 11)   # la esquina de arriba a la derecha de la sala de 8 x 12


def pasos_hasta_la_meta(pos: tuple[int, int]) -> int:
    """Cuantos pasos faltan hasta la meta, contando por la rejilla.

    Se la dejo hecha para que no pierda tiempo en esto. Usela o no la use.
    """
    return abs(pos[0] - META[0]) + abs(pos[1] - META[1])


# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · VERSION 1
# ═══════════════════════════════════════════════════════════════════════════
#
# Hipotesis (antes de ejecutar):
#   Premiar al agente por moverse arriba o a la derecha (hacia la meta), y
#   penalizar por moverse abajo o a la izquierda con un castigo MAS GRANDE que
#   el premio (factor 1.5), para que un vaiven de ida y vuelta no le deje
#   ganancia neta. El tamano del premio/castigo escala con pasos_restantes:
#   alto al empezar (lejos de la meta), bajo cuando ya casi llega.
#   Expectativa: el agente deberia llegar a la meta casi siempre, y no
#   quedarse dando vueltas cerca de ella para cobrar recompensa gratis.
#
# Resultado real (uv run pytest tests/test_reto3.py):
#   4 de 5 pruebas pasan, incluida la que mas preocupaba
#   (test_dar_una_vuelta_completa_no_deja_ganancia): un ciclo cuadrado ya NO
#   deja ganancia gratis, asi que el "vicio" del vaiven si se corrigio.
#
#   Pero la version mas exigente (test_con_gamma_uno_el_ciclo_suma_
#   exactamente_cero) SI falla: el mismo ciclo cuadrado deja -3.75 de
#   "ganancia", cuando tendria que dar cerca de 0. Para comparar: un solo paso
#   en el entorno real cuesta -0.04. La pista pesa casi 100 veces mas que el
#   problema original.
#
# Lo que esto sugiere (sin arreglarlo todavia):
#   El castigo mas grande que el premio resolvio el problema de "cobrar
#   gratis por dar vueltas", pero lo sobre-corrigio: ahora cualquier paso
#   hacia atras, en cualquier parte del mapa, se castiga con una magnitud
#   enorme comparada con la recompensa real del problema. Falta ver si eso
#   hace que el agente resuelva EL PROBLEMA ORIGINAL o un problema distinto,
#   dominado casi por completo por mi funcion en vez de por el entorno.
#
def mi_moldeado(
    anterior: tuple[int, int] | None,
    siguiente: tuple[int, int],
    terminal: bool,
) -> float:
    """La recompensa extra de una transicion. **Esto es lo que usted escribe.**"""
    # ── su respuesta va aqui ──────────────────────────────────────────────
    if anterior is None:
        return 0.0

    fue_arriba = siguiente[0] < anterior[0]
    fue_derecha = siguiente[1] > anterior[1]
    fue_abajo = siguiente[0] > anterior[0]
    fue_izquierda = siguiente[1] < anterior[1]

    # Cuanto le faltaba ANTES de moverse: alto al empezar, bajo cerca de la meta.
    pasos_restantes = pasos_hasta_la_meta(anterior)

    if fue_arriba or fue_derecha:
        return ESCALA * pasos_restantes
    if fue_abajo or fue_izquierda:
        return -PENALIZACION * ESCALA * pasos_restantes
    return 0.0   # se quedo en el mismo sitio (choco contra el borde)
