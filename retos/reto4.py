"""Reto de la sesion 4 · Un agente que se rinde.

═══════════════════════════════════════════════════════════════════════════
QUE PASA
═══════════════════════════════════════════════════════════════════════════

El actor-critico de ``rlrs.pg`` colapsa en la mitad de las semillas. No
aprende despacio: **deja de aprender**. Lo viste en la parte 4 del
experimento:

    tramo             retorno medio   desviacion   llegan a la meta
    0 a 100                 -3.5056       0.9940                25 %
    200 a 300               -3.9776       0.2229                 1 %
    500 a 600               -4.0000       0.0000                 0 %

La columna que importa es la de la desviacion. Cuando llega a cero, todos los
episodios dan lo mismo, y un metodo que aprende comparando episodios se queda
sin nada que comparar.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

Dos cosas, y la primera se entrega aunque la segunda no salga.

1. **El diagnostico, escrito en tu bitacora antes de tocar el codigo.** Por
   que crees que pasa. Que cantidad se hace cero primero. Por que no se
   arregla con mas episodios.

2. **El arreglo.** Rellena ``mi_agente`` para que no colapse en ninguna
   semilla. Tienes todas las piezas de ``rlrs.pg`` disponibles y puedes mover
   lo que quieras: el metodo, la tasa de aprendizaje, la linea base, el
   tamano del lote, el termino de entropia.

    uv run python scripts/reto4.py        lo evalua con semillas que no ves
    uv run pytest tests/test_reto4.py     comprueba el contrato

═══════════════════════════════════════════════════════════════════════════

Una pista que no es una respuesta: el problema no esta en cuanto aprende, sino
en que deja de haber informacion que aprender. Cualquier arreglo tiene que
atacar eso.
"""

from __future__ import annotations

from rlrs.pg import EntrenamientoPG, actor_critico, reinforce  # noqa: F401


# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · DIAGNOSTICO (antes de tocar el codigo)
# ═══════════════════════════════════════════════════════════════════════════
#
# Que cantidad se hace cero primero:
#   La VENTAJA. En actor_critico, `ventaja = g - valores` (el retorno real
#   del episodio menos lo que el critico esperaba). Cuando la politica se
#   vuelve casi determinista, todos los episodios terminan dando exactamente
#   el mismo retorno, y el critico ya aprendio a predecir ese mismo numero
#   -> `g - valores = 0`, en todos los pasos, no en algunos.
#
# Por que eso frena el aprendizaje:
#   El gradiente del actor se multiplica por esa ventaja
#   (`grad *= ventaja[:, None] / len(acciones)`). Ventaja cero en todos los
#   pasos -> gradiente literalmente cero -> los pesos no se mueven ni un poco.
#   No es un declive lento (los numeros no bajan "cada vez un poco mas"): es
#   un choque contra el peor resultado posible (-4.0000, agotar el episodio
#   sin llegar nunca) y despues una linea plana, porque ya no hay a donde
#   bajar mas.
#
# Por que no se arregla con mas episodios:
#   Si el episodio 501 es una copia identica del 500 (la politica ya no tiene
#   azar real que la haga variar), jugar 500 episodios mas repite la misma
#   "pregunta sin respuesta nueva" 500 veces. Cero por cualquier cantidad de
#   repeticiones sigue siendo cero: hace falta que algo vuelva a introducir
#   variacion entre episodios, no mas tiempo del mismo.
#
# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · EL ARREGLO Y POR QUE FUNCIONA
# ═══════════════════════════════════════════════════════════════════════════
#
# El arreglo: entropia=0.03 en actor_critico, sin tocar ningun otro parametro.
#
# Por que funciona: la entropia busca justamente que el agente no se estanque
# cuando la ventaja de un episodio termina siendo igual a lo que ya se venia
# evaluando. Le suma a la correccion del actor un empujon extra para que no
# pierda la intencion de probar otras acciones, sin que la intencion de "ir
# siempre a la jugada segura" termine predominando por completo. Eso mantiene
# viva la variacion entre episodios, y por eso la ventaja (g - valores) no se
# queda clavada en cero.
#
# Se llego a 0.03 probando los dos extremos, no adivinando:
#   - entropia=0.3 (muy por encima del piso): concentracion 0.35-0.43 (casi
#     azar puro), 2 semillas de 6 siguen marcando COLAPSA, y media -0.8553.
#     El agente no perdio la intencion de probar, pero esa intencion paso a
#     predominar tanto que nunca aprendio un camino confiable.
#   - entropia=0.03 (apenas por encima del piso de la guia, 0.01): concen-
#     tracion 0.91-0.96 en las 6 semillas, 0 colapsos, media +0.5732 (por
#     encima del minimo +0.45). Suficiente empujon para no quedarse pegado
#     en cero, suficiente confianza para converger a una buena politica.
#
def mi_agente(env, phi, episodes: int, gamma: float, seed: int) -> EntrenamientoPG:
    """Entrena un agente de gradiente de politica que no colapse.

    Tiene que devolver lo que devuelven ``actor_critico`` o ``reinforce``, es
    decir un ``EntrenamientoPG``. Lo que hagas por dentro es cosa tuya.

    Parameters
    ----------
    env, phi:
        El entorno y la funcion de caracteristicas. Se los pasa el arnes.
    episodes, gamma, seed:
        Hay que respetarlos. Entrenar mas episodios de los que te dan, o con
        otra semilla, no cuenta como arreglo.
    """
    # ── tu respuesta va aqui ──────────────────────────────────────────────

    return actor_critico(env, phi, episodes=episodes, gamma=gamma, seed=seed, entropia=0.03)
