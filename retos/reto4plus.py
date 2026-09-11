from __future__ import annotations

import numpy as np
from rlrs.pg import EntrenamientoPG, actor_critico, reinforce  # noqa: F401
from rlrs.aprox import caracteristicas_posicion
from rlrs.envs import GridWorld
from rlrs.shaping import retorno_verdadero

EPISODIOS = 1200
GAMMA = 0.9
SEMILLAS = range(6)
UMBRAL_COLAPSO = -1.0
MINIMO_MEDIA = 0.45

VALORES = [0.01, 0.02, 0.03, 0.05, 0.10, 0.20]


def rejilla():
    return GridWorld(noise=0.2, step_reward=-0.04)


def evaluar(entropia):
    reales = []

    for semilla in SEMILLAS:
        env = rejilla()
        ap = actor_critico(env, 
                           caracteristicas_posicion(env), 
                           episodes=EPISODIOS,
                           gamma=GAMMA,
                           seed=semilla,
                           entropia=entropia)

        politica = ap.politica(rejilla(), caracteristicas_posicion(rejilla()))
        real, _, _ = retorno_verdadero(rejilla(), politica, episodios=100)
        reales.append(real)

    a = np.array(reales)
    colapsos = int((a < UMBRAL_COLAPSO).sum())

    return a.mean(), colapsos, a.min()

for e in VALORES:
    media, colapsos, peor = evaluar(e)
    print(f"entropia={e:<6} media={media:+.4f}  colapsos={colapsos}  peor={peor:+.4f}")
