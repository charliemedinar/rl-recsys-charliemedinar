"""Reto de la sesion 6 · Gane a dos lineas de codigo.

═══════════════════════════════════════════════════════════════════════════
QUE PASA
═══════════════════════════════════════════════════════════════════════════

Sobre los datos de ASSISTments, con particion TEMPORAL, esto es lo que sale:

    recomendador                 Recall@10   nDCG@10   cobertura
    repetir lo propio               0,7009    0,5880       0,973
    popularidad                     0,4121    0,2738       0,090
    kNN por items                   0,2613    0,1857       0,856
    al azar                         0,0990    0,0683       1,000
    novedad pura                    0,0949    0,0766       0,649

Lea la primera fila y la tercera. **El filtro colaborativo pierde contra una
linea base de dos lineas**, y por casi tres veces. Y «repetir lo propio» es
literalmente esto:

    los items que este usuario ya practico, el mas repetido primero,
    y despues los mas populares para rellenar

Lea tambien la ultima fila. «Novedad pura», que solo recomienda cosas que el
usuario NO ha hecho, saca menos que recomendar AL AZAR. La intuicion de que un
recomendador no debe repetir es, en estos datos, el error mas caro posible.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

Dos cosas, y la primera se entrega aunque la segunda no salga.

1. **El diagnostico, escrito en su bitacora antes de tocar el codigo.** Por que
   gana repetir. Que dice eso sobre estos datos. Y una prediccion: cuanto cree
   que va a sacar su recomendador.

2. **El recomendador.** Rellene ``mi_recomendador`` para superar a «repetir lo
   propio» sin encoger el catalogo. Tiene todo ``rlrs.recomendacion``
   disponible y puede escribir el suyo desde cero.

    uv run python scripts/reto6.py        mide y da el veredicto
    uv run pytest tests/test_reto6.py     comprueba el contrato

═══════════════════════════════════════════════════════════════════════════

Aviso: hay una forma facil de subir el Recall que consiste en recomendarle a
todo el mundo lo mismo. Por eso hay un criterio de cobertura, y por eso el
arnes le ensena las cuatro cifras y no una.
"""

from __future__ import annotations

from rlrs.recomendacion import (  # noqa: F401
    Particion,
    factorizacion_implicita,
    knn_items,
    por_popularidad,
    repetir_lo_propio,
)


# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · DIAGNOSTICO (antes de tocar el codigo)
# ═══════════════════════════════════════════════════════════════════════════
#
# Por que gana "repetir lo propio":
#   Los datos estan muy concentrados: 10 de 111 habilidades se llevan el
#   36.2% de todas las interacciones. Eso hace que "lo que el estudiante ya
#   practico mucho" sea una apuesta muy fuerte sobre lo que va a practicar
#   despues. Y el relleno de la lista, cuando se acaban sus propias
#   habilidades, no es al azar: usa popularidad global, que tampoco es una
#   apuesta debil, porque lo mas popular es justamente lo que la mayoria de
#   estudiantes termina practicando de todas formas. Las dos partes de la
#   lista (lo propio + el relleno popular) apuntan en la misma direccion.
#
# Por que pierde kNN por items, y por tanto:
#   kNN calcula la similitud entre dos habilidades contando cuantos
#   estudiantes practicaron las dos. Con los datos tan concentrados en pocas
#   habilidades, la mayoria de los pares de habilidades del catalogo (101 de
#   111 se reparten apenas el 64% restante) casi no tienen coincidencias
#   suficientes para calcular una similitud confiable. El mapa de vecinos
#   queda armado con muy poca evidencia para la mayor parte del catalogo, y
#   una similitud calculada con pocos datos es mas ruido que señal.
#
# La conexion entre las dos:
#   Es la MISMA cifra (la concentracion de las interacciones en pocas
#   habilidades) la que explica las dos cosas a la vez, desde angulos
#   opuestos: le regala la victoria a "repetir lo propio" y le arruina el
#   mapa de similitud a kNN.
#
# Prediccion (Version 1, antes de ejecutar):
#   Se va a probar factorizacion_implicita. La eleccion prioriza que aparezca
#   el item relevante sobre en que posicion aparece: el reto solo exige
#   Recall@10 y cobertura, no nDCG.
#
#   Recall@10 esperado: ~0.72. Ya se midio este mismo modelo (32 factores) en
#   el Taller B, sobre esta misma particion temporal, y saco 0.7179 - por
#   encima del listón de 0.7100.
#
#   Cobertura esperada: alta, mas cerca de kNN (0.856) que de popularidad
#   (0.090). A diferencia de popularidad, que siempre devuelve el mismo top
#   fijo para todo el mundo, factorizacion calcula un puntaje personalizado
#   para TODO el catalogo por cada usuario, asi que distintos usuarios deberian
#   terminar recibiendo distintos items en su lista.
#
# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · RESULTADOS (version 1, con uv run python scripts/reto6.py)
# ═══════════════════════════════════════════════════════════════════════════
#
#   SU RECOMENDADOR   Recall@10 0.7142   nDCG@10 0.5634   cobertura 0.982
#   repetir lo propio Recall@10 0.7011   nDCG@10 0.5862   cobertura 0.964
#
#   SUPERADO. Recall@10 = 0.7142 (listón 0.7100) y cobertura = 0.982
#   (listón 0.50), las dos condiciones a la vez.
#
# Contra la prediccion:
#   Recall@10: se predijo ~0.72, salio 0.7142. Muy cerca - el numero medido
#   en el Taller B (0.7179) era con la misma configuracion casi exacta, y la
#   pequeña diferencia es solo el efecto de la semilla por defecto.
#   Cobertura: se predijo "alta, mas cerca de kNN (0.856) o mejor". Salio
#   0.982, incluso mas alta de lo esperado - casi todo el catalogo (109 de
#   111 items) llega a aparecer en alguna recomendacion.
#
# Lo que se repite del Taller B, ahora con este numero exacto:
#   Igual que factorizacion contra repetir_lo_propio en el taller, aqui GANA
#   en Recall (0.7142 frente a 0.7011) y PIERDE en nDCG (0.5634 frente a
#   0.5862). Encuentra mas items relevantes, los ordena peor. El reto 6 solo
#   exige Recall y cobertura, por eso esa perdida en nDCG no impide superar
#   el listón - pero si el criterio hubiera sido nDCG, esta misma solucion
#   habria perdido contra las "dos lineas de codigo".
#
# Nota aparte, sobre la particion:
#   El arnes tambien midio este mismo recomendador con particion ALEATORIA en
#   vez de temporal: el nDCG sube de 0.5634 a 0.8395, un 49% mas alto, sin
#   cambiar una sola linea de codigo. Es el mismo recomendador; lo unico que
#   cambio fue que la particion aleatoria deja ver "el futuro" del usuario
#   mezclado con su pasado. Un recordatorio de por que la particion se elige
#   ANTES que el modelo (Taller A) y se declara junto con cualquier cifra.
#
def mi_recomendador(particion: Particion):
    """Devuelve una funcion que recomienda. **Esto es lo que usted escribe.**

    Parameters
    ----------
    particion:
        Tiene ``train`` (la lista de historiales que SI se pueden mirar),
        ``n_items`` y ``nombre``. **No tiene el conjunto de prueba**, y esa
        ausencia es lo unico que impide hacer trampa sin querer.

    Returns
    -------
    callable
        Recibe el historial de un usuario, como arreglo de items, y devuelve
        una lista de items ordenada de mejor a peor.
    """
    # ── su respuesta va aqui ──────────────────────────────────────────────
    return factorizacion_implicita(particion, factores=32)
