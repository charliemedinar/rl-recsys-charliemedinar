"""Reto de la sesion 5 · La politica que se queda clavada.

═══════════════════════════════════════════════════════════════════════════
QUE PASA
═══════════════════════════════════════════════════════════════════════════

Meridiano visto como bandido: veinte brazos, uno por habilidad, y en cada
ronda se elige uno. La politica avida pura hace lo obvio, que es quedarse con
el brazo que mejor le ha ido. Y le pasa esto:

    rondas    avida pura      UCB1      quien gana
        25       +0,0118    +0,0107      empatan
       100       +0,0160    +0,0393      UCB1, y por el doble
       500       +0,0160    +0,1933      UCB1, y por doce veces
      1500       +0,0160    +0,2092      UCB1, y por trece

Lea la columna de la avida despacio. **De la ronda 100 a la 1500 no gana ni
una milesima.** Mil cuatrocientas rondas mas y el mismo numero, hasta el cuarto
decimal. Se quedo clavada, y toca 2,3 brazos de veinte.

Y fijese en la primera fila: con veinticinco rondas **empata** con UCB1. No es
una politica tonta, es una politica con prisa. El problema aparece despues.

Lo que le pasa es que en cuanto un brazo le da algo, deja de mirar los demas, y
ese brazo **se agota**, porque el estudiante ya domina esa habilidad y
practicarla otra vez ya no le ensena nada. La avida se queda cobrando de un
pozo seco.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

Dos cosas, y la primera se entrega aunque la segunda no salga.

1. **El diagnostico, escrito en tu bitacora antes de tocar el codigo.** Por
   que se queda clavada. Que le pasa al brazo elegido a medida que se tira de
   el. Y una prediccion: cuanto crees que va a ganar tu arreglo.

2. **El arreglo.** Rellena ``mi_politica`` con una politica de bandido que
   reparta mejor las tiradas. Tienes ``epsilon_avida``, ``ucb1``, ``thompson``
   y ``linucb`` en ``rlrs.bandidos``, y puedes escribir la tuya desde cero si
   prefieres.

    uv run python scripts/reto5.py        entrena y mide, e imprime el veredicto
    uv run pytest tests/test_reto5.py     comprueba el contrato

═══════════════════════════════════════════════════════════════════════════

Aviso, y va en serio: hay una linea base tonta que va a costar mucho superar,
y descubrir cual es vale mas que superarla. Cuando la vea, anotela en la
bitacora antes de intentar ganarle.
"""

from __future__ import annotations

from rlrs.bandidos import (  # noqa: F401
    Corrida,
    avida,
    epsilon_avida,
    linucb,
    thompson,
    ucb1,
)


# ═══════════════════════════════════════════════════════════════════════════
# BITACORA · DIAGNOSTICO (antes de tocar el codigo)
# ═══════════════════════════════════════════════════════════════════════════
#
# Por que la avida pura se queda clavada:
#   Se enfoca casi por completo en un solo brazo desde las primeras rondas, y
#   deja de mirar los demas en cuanto ese brazo le da un resultado que le
#   parece bueno.
#
# Que le pasa al brazo elegido a medida que se tira de el:
#   MeridianoBandido cambia la distribucion del brazo al tirar de el: cada vez
#   que se practica una habilidad, el estudiante aprende y su probabilidad de
#   acierto sube. Pero esa subida tiene techo (rendimientos decrecientes,
#   como llenar un vaso: los primeros intentos suben mucho, y cerca del techo
#   cada intento adicional sube cada vez menos). Como la avida repite siempre
#   el mismo brazo, esa habilidad llega rapido cerca de su techo, y a partir
#   de ahi cada repeticion ya casi no aporta nada nuevo.
#
# Por que el numero final es tan BAJO, no solo por que queda plano:
#   La ganancia se mide como el dominio promedio de las 20 habilidades. Si
#   solo una llega a su techo y las otras 19 nunca se tocan, se quedan
#   exactamente en su punto de partida. El promedio de las 20 casi no se
#   mueve, aunque esa unica habilidad si haya mejorado mucho. Todo el
#   potencial de mejora de las otras 19 queda sin tocar.
#
# Por que no se arregla con mas rondas:
#   De la ronda 100 a la 1500 (1400 rondas mas) la ganancia no se mueve ni
#   una milesima: +0,0160 en las dos. Una vez que la avida se pego a un
#   brazo ya casi agotado, nada en su regla de decision la empuja a probar
#   otro: repetir la misma jugada, muchas veces mas, no genera ninguna
#   informacion nueva sobre las 19 habilidades sin tocar.
#
# Prediccion (probando UCB1):
#   UCB1 no es aleatorio: no tira ningun dado (salvo para desempatar), su
#   exploracion es calculada. Por sus caracteristicas, va a intentar visitar
#   los brazos poco usados o sin usar. Espero que, a medida que avancen las
#   iteraciones, todos los brazos disponibles se recorran al menos unas
#   pocas veces cada uno. Eso deberia ayudar a cumplir la metrica de brazos
#   usados. Sobre la ganancia (cuanto aprende), espero un margen razonable,
#   ya que al visitar tantos brazos deberia aprender de mas habilidades
#   disponibles.
#
#   Nota adicional: `ucb1` tira una vez de cada brazo antes de aplicar su
#   formula (ver `if sin_tirar.size:` en rlrs/bandidos.py), asi que los 20
#   brazos quedan tocados al menos una vez desde el arranque, sin depender
#   de la suerte - la metrica de brazos usados (>= 15/20) deberia quedar
#   practicamente asegurada por diseño.
#
#   Nota de cautela sobre la ganancia: la propia guia de la sesion ya midio
#   esto en Meridiano (no en el bandido de libro) y el resultado fue mas
#   ajustado de lo esperado: UCB1 saco +0,1933 y tirar al azar saco +0,1569,
#   con intervalos que se solapan. En el bandido de libro (brazos fijos) UCB1
#   le ganaba a la avida por 12 veces, pero aqui, con brazos que se agotan,
#   puede que no se separe con claridad del azar.
#
# Por que se descarta Thompson para este reto:
#   La recompensa de Meridiano en modo "dominio" es un numero real (con
#   decimales), no un resultado de acierto/fallo, y ademas puede ser
#   NEGATIVA (se comprobo corriendolo: crasheo con -0,2086 en las primeras
#   rondas). Thompson, tal como esta escrito, usa una creencia Beta, que por
#   definicion matematica solo representa probabilidades entre 0 y 1 - no
#   admite valores continuos ni negativos. No es un fallo de implementacion:
#   es que la Beta es la creencia conjugada de una Bernoulli, y "dominio" no
#   es una Bernoulli.
#   Este mismo problema aparece en otros dominios donde la recompensa es una
#   ganancia o perdida real, no un simple si/no - por ejemplo, en bandidos
#   aplicados a trading. Ahi se usa una version de Thompson con una creencia
#   distinta (tipicamente una Normal en vez de una Beta), que si admite
#   numeros continuos y negativos. La idea general de Thompson (mantener una
#   creencia y muestrear de ella) se mantiene; lo que cambia es la forma
#   matematica de la creencia, segun que tipo de numero es la recompensa.
#   Adaptarlo asi seria una decision de diseno bastante mas grande que lo que
#   pide este reto, asi que se descarta por ahora y se sigue con UCB1.
#
def mi_politica(bandido, rondas: int, seed: int) -> Corrida:
    """Elige un brazo en cada ronda. **Esto es lo que usted escribe.**

    Parameters
    ----------
    bandido:
        Tiene ``n_brazos`` y ``tirar(brazo, rng) -> recompensa``. Nada mas. No
        hay estado que consultar: esa es toda la gracia de un bandido.
    rondas:
        Cuantas veces se elige. Hay que hacer exactamente esas.
    seed:
        La semilla. Dos llamadas con la misma semilla tienen que dar lo mismo.

    Returns
    -------
    Corrida
        Lo que devuelven las politicas de ``rlrs.bandidos``.
    """
    # ── su respuesta va aqui ──────────────────────────────────────────────
    return avida(bandido, rondas, seed=seed)
