# Taller B — una cifra no es un resultado

Notas propias para presentar el tramo B2-B3 del Taller B, Sesión 6 (sábado 12
de septiembre). Lo dirigen los grupos 3 y 4; a Grupo 4 (nosotros) nos toca
"la práctica y el cierre": ejecutar en pantalla, dirigir la discusión de B2,
hacer votar al curso, y presentar B3.

## 0. Contexto de la sesión completa (por qué existe este taller)

Esto no es un ejercicio suelto: es una de tres piezas de un mapa que arma el
profesor en unos 50 minutos de exposición, y el resto (casi 4 horas) lo
dirigen los grupos de proyecto en tres talleres seguidos.

| hora | qué pasa | quién |
|---|---|---|
| 08:00 | Apertura: de bandidos a recomendación | El profesor |
| 08:50 | Preparación de cada taller | Cada pareja, por su cuenta |
| 09:50 | Taller A · La partición decide quién gana | Grupos 5 y 6 |
| 10:50 | **Taller B · Una cifra no es un resultado** | **Grupos 3 y 4** |
| 11:40 | Taller C · La línea base que humilla al modelo | Grupos 1 y 2 |
| 12:30 | Cierre: las tres reglas juntas, el reto 6 | El profesor |

### De bandidos a recomendación

La sesión anterior (bandidos) dejó la idea de "decidir sin estado, con
recompensa". Hoy se le devuelven dos cosas que un bandido no tenía:

| | bandido (sesión anterior) | recomendador (hoy) | qué se rompe |
|---|---|---|---|
| Brazos | 20 | Miles o millones (un ítem del catálogo = un brazo) | No hay tiempo de probar cada uno |
| Jugador | Siempre el mismo | Uno distinto en cada visita | Lo aprendido de uno no sirve para el siguiente, salvo que se parezcan |
| Recompensa | Se ve al instante | Se ve a veces, y tarde | Un clic no es "me gustó"; no hacer clic no es "no me gustó" |
| Datos | Los genera la propia política | Los generó **otra** política, hace años | Lo que hay en el registro es lo que un sistema anterior puso delante |

La fila que más importa es la última: **sesgo de exposición**. Los datos de
hoy (ASSISTments) no los generó nuestra política — los generó el tutor de
entonces, con sus propios criterios, y solo se ve realimentación de lo que
ese sistema decidió mostrar. Esto no se arregla midiendo mejor: se declara.

### Los datos, en números

```
3,091 estudiantes con 10 o mas interacciones
111 habilidades en el catalogo
320,582 interacciones
```

Las diez habilidades más practicadas concentran el 36.2 % de todas las
interacciones. La lectura fácil es "esas son las más importantes". Es la
lectura que hay que resistir: **no dice que gusten más, dice que el tutor de
entonces las puso más**. Es la misma idea del sesgo de exposición, ya
convertida en un número concreto.

### Las tres decisiones del sábado (y dónde encaja el Taller B)

Cada taller resuelve una decisión, y las tres van **antes** de elegir
modelo — ese orden es lo que se lleva el bloque entero.

| decisión | la pregunta | taller |
|---|---|---|
| Qué se esconde | ¿Cómo separo lo que el modelo ve de lo que tiene que adivinar? | A · grupos 5 y 6 |
| **Cómo se juzga** | **¿Qué cifra decide quién gana, y qué deja fuera esa cifra?** | **B · grupos 3 y 4** |
| Contra qué se compara | ¿Cuál es la tontería más simple que ya resuelve el problema? | C · grupos 1 y 2 |

*"Primero la partición. Después la métrica. Después la línea base. Y solo
entonces el modelo."* Nuestro taller (B) es el segundo paso: ya viene con los
datos partidos (Taller A), y responde **cómo se juzga** un recomendador antes
de construir ninguno.

El enlace que da el profesor justo antes de nuestro taller, para que se
entienda por qué B1 empieza sin computador:

> *"Acabamos de ver que la forma de partir los datos cambia quién gana. Los
> grupos 3 y 4 traen algo peor: con los datos bien partidos, y sin tocar
> nada, la cifra que elijan cambia quién gana."*

---

## 1. B1 · Los mismos aciertos, en distinto sitio (la conduce Grupo 3)

Aritmética de pizarra, sin datos ni modelos. Un estudiante va a practicar
mañana tres habilidades: la 7, la 42 y la 99. Dos recomendadores proponen
diez cosas cada uno, con **los mismos diez elementos**, solo que en distinto
orden:

- A: `[7, 42, 99, 1, 2, 3, 4, 5, 6, 8]` — los tres aciertos primero.
- B: `[1, 2, 3, 4, 5, 6, 8, 7, 42, 99]` — los tres aciertos al final.

| recomendador | Recall@10 | nDCG@10 |
|---|---|---|
| A · aciertos arriba | 1.0000 | 1.0000 |
| B · aciertos abajo | 1.0000 | 0.4250 |

Mismo Recall (los dos encontraron los 3: para el Recall una lista de diez es
una bolsa de diez, no hay orden). El nDCG de A es 2.35 veces el de B, porque
cada acierto vale `1/log2(posición + 1)` — premia mucho estar arriba, casi
nada estar al fondo. El remate de B1: *"dos sistemas idénticos según una
cifra, y donde uno vale más del doble que el otro según otra — y todavía no
hemos mirado ningún dato real."*

---

## 2. B2 · Cada uno gana una métrica (la dirigimos nosotros)

### El enunciado

> Mismos dos recomendadores, ejecutados sobre los datos reales de
> ASSISTments.
>
> **Pregunta 2, y esta se vota:** "Tienen que poner uno de los dos en
> producción mañana. ¿Cuál, y para qué producto?"
>
> No se cierra el debate en el momento. El cierre que hay que dejar dicho es:
> *"la respuesta no está en la tabla, está en el producto, y por eso la
> métrica se elige antes"*.

### Los datos reales (de `uv run python talleres/taller_b_metricas.py`)

3,091 usuarios evaluables, partición temporal (se esconde el final de cada
historial — la del Taller A).

| recomendador | Recall@10 | nDCG@10 |
|---|---|---|
| factorización (32 factores) | 0.7179 | 0.5652 |
| repetir lo propio | 0.7011 | 0.5862 |
| popularidad | 0.4121 | 0.2738 |
| kNN por ítems (20) | 0.2613 | 0.1857 |

Las dos primeras filas son las que importan para B2: **factorización gana en
Recall, repetir lo propio gana en nDCG.** Los dos pueden decir que ganaron, y
los dos tienen razón.

### Qué es cada uno de los dos modelos (sin fórmulas)

**Repetir lo propio.** Mira solo el historial de ESE estudiante — qué
habilidades practicó y cuántas veces — y devuelve esas mismas, las más
repetidas primero. Si hace falta rellenar la lista, usa lo más popular entre
todos. No aprende nada de otros estudiantes: es contar y ordenar.

Analogía: un bibliotecario que solo mira tu propio historial de préstamos, ve
que sacaste el mismo libro cinco veces, y te lo vuelve a ofrecer. Nunca te va
a sugerir algo que tú mismo no hayas tocado antes (salvo el relleno
genérico).

**Factorización implícita.** Mira a todos los estudiantes a la vez. Aprende,
para cada estudiante y cada habilidad, un perfil de números tal que
comparando el perfil del estudiante con el de una habilidad se puede predecir
qué tan probable es que la practique — aunque nunca la haya tocado antes.
Aprende patrones como "quienes practicaron A y B, después practicaron C". Es
el método de Hu, Koren y Volinsky (2008): la confianza en cada interacción
crece con cuántas veces se repitió (`c = 1 + α·r`), porque en realimentación
implícita no hay negativos — que alguien no haya practicado algo no dice que
no le sirva, solo que no se lo pusieron.

Analogía: el mismo bibliotecario, pero mirando el historial de TODOS los
lectores, y notando patrones entre lectores parecidos para sugerirte algo que
tú nunca has tocado.

### Por qué eso produce justo ese resultado (mecanismo)

- **Por qué factorización gana Recall:** "repetir lo propio" solo puede
  recomendar cosas que el estudiante ya hizo antes (más el relleno popular).
  Si lo que va a practicar mañana es algo nuevo para él, "repetir lo propio"
  no lo puede encontrar nunca — está limitado a su pasado. Factorización sí
  puede proponer algo nunca antes tocado por ese estudiante, porque lo dedujo
  del comportamiento de estudiantes parecidos. Por eso encuentra más cosas en
  total.

- **Por qué repetir lo propio gana nDCG:** cuando "repetir lo propio"
  acierta, acierta con mucha certeza (es casi obvio que el estudiante repita
  lo que ya venía repitiendo mucho), así que sus aciertos tienden a quedar
  arriba, en el puesto 1 o 2. Factorización acierta con base en patrones
  estadísticos sobre otros estudiantes, no en certeza sobre este estudiante
  en particular — cuando acierta, no siempre sabe cuál de sus aciertos poner
  primero, y algunos quedan enterrados varios puestos más abajo.

### Ejemplo de referencia (inventado, para ver el mecanismo paso a paso)

No son datos reales — son un ejemplo armado a mano, a propósito, para que se
parezca en dirección y magnitud a las cuatro cifras reales de arriba.

Un estudiante va a practicar mañana, de verdad, estas tres habilidades (lo
escondido, el conjunto relevante): **fracciones, área de triángulos,
ecuaciones lineales**. Antes venía practicando mucho multiplicación y
división.

**Lo que propone "repetir lo propio" (10 ítems):**

```
1. fracciones                 ← acierto
2. ecuaciones lineales        ← acierto
3. multiplicación
4. división
5. resta
6. suma
7. potencias
8. raíces
9. geometría básica
10. porcentajes
```

Encuentra 2 de los 3, y los dos casi arriba de todo. "Área de triángulos"
nunca aparece: el estudiante nunca la tocó y no es tan popular como para
colarse en el relleno.

**Lo que propone "factorización" (10 ítems):**

```
1. fracciones                 ← acierto
2. potencias
3. raíces
4. multiplicación
5. geometría básica
6. porcentajes
7. área de triángulos         ← acierto
8. división
9. resta
10. ecuaciones lineales       ← acierto
```

Encuentra los 3, pero dos quedan enterrados: en el puesto 7 y en el puesto
10.

**Recall** — solo pregunta cuántos de los 3 aparecieron en algún lugar del
top 10, sin importar dónde:

- repetir lo propio: 2 de 3 → **0.6667**
- factorización: 3 de 3 → **1.0000**

Factorización gana. Encontró más.

**nDCG** — cada acierto aporta `1 / log2(posición + 1)`, y se divide entre el
ideal (los 3 aciertos en los puestos 1, 2 y 3):

```
ideal = 1/log2(2) + 1/log2(3) + 1/log2(4) = 1.0000 + 0.6309 + 0.5000 = 2.1309
```

- repetir lo propio: aciertos en 1 y 2
  `(1/log2(2) + 1/log2(3)) / 2.1309 = (1.0000 + 0.6309) / 2.1309 = 0.7654`

- factorización: aciertos en 1, 7 y 10
  `(1/log2(2) + 1/log2(8) + 1/log2(11)) / 2.1309 = (1.0000 + 0.3333 + 0.2891) / 2.1309 = 0.7602`

Repetir lo propio gana, por poco — exactamente el mismo patrón cerrado que
las cifras reales (0.5862 contra 0.5652): lo poco que encuentra, lo pone
donde de verdad importa; lo que encuentra de más, lo entierra.

### Los dos argumentos para la votación (sin inclinar la respuesta)

- **A favor de factorización:** si el usuario va a mirar la lista completa
  (una lista larga de ejercicios que revisa entera), lo que importa es que lo
  bueno esté ahí en algún lugar, no en qué posición exacta.
- **A favor de repetir lo propio:** si el usuario solo mira las primeras 2-3
  cosas y se va (un carrusel, una notificación), lo que importa muchísimo es
  qué está arriba — y ahí repetir lo propio gana.

---

## 3. B3 · La k también decide

### Los datos reales

| k | factorización | repetir lo propio | gana |
|---|---|---|---|
| 1 | 0.4151 | 0.4879 | repetir lo propio |
| 3 | 0.5060 | 0.5572 | repetir lo propio |
| 5 | 0.5863 | 0.6163 | repetir lo propio |
| 10 | 0.7179 | 0.7011 | factorización |
| 20 | 0.8272 | 0.7827 | factorización |

### Por qué se voltea el ganador (el mecanismo)

`repetir_lo_propio` arma su lista en dos bloques pegados: primero lo propio
del estudiante (personalizado, casi seguro), y cuando se le acaba, rellena
con popularidad global (genérico, igual para todos). `factorización` no
tiene ese quiebre: toda su lista, de principio a fin, sale del mismo cálculo
personalizado.

- **k chico (1, 3, 5):** solo se ve el primer tramo de cada lista. Para
  "repetir lo propio" ese tramo es su parte fuerte (lo casi-seguro). Para
  factorización, ese mismo tramo trae sus apuestas más arriesgadas, que no
  todas aciertan tan rápido. Gana el modelo "tonto pero seguro".
- **k grande (10, 20):** ya se alcanza a ver el tramo donde "repetir lo
  propio" entró en su relleno genérico, mientras factorización sigue
  proponiendo apuestas personalizadas hasta el final — algunas de las cuales
  sí eran correctas pero estaban enterradas (lo mismo que en el ejemplo de
  B2). Factorización se despega.

### La conexión con bandidos (hay que decirla así)

*"Ayer vimos que una política de bandido es mejor a partir de cierto
horizonte: la ávida ganaba a cien rondas y perdía a dos mil. Miren la columna
de la derecha: repetir lo propio gana hasta k=5, factorización gana desde
k=10. Es el mismo fenómeno con otro nombre — aquí el horizonte no es el
número de rondas, es cuántos ítems caben en la pantalla. Y eso lo decide un
diseñador, no un investigador."*

`repetir_lo_propio` es como la ávida: rinde rápido con poco presupuesto, pero
su fuente de aciertos personalizados es finita y no tiene margen para seguir
sumando. `factorización` es como UCB1: no arranca con la misma ventaja
inmediata, pero cada ítem adicional que se muestra es una oportunidad más de
que una apuesta "enterrada" entre a contar.

**Ejercicio en vivo (minutos 40-44):** que el curso busque su punto de cruce
entre k=5 y k=10 (¿en k=7 quién gana?). Cambiar la k es cambiar un número en
la tupla del bucle en `taller_b_metricas.py`.

---

## 4. El cierre (minutos 44-50, lo conduce Grupo 4)

**La regla del taller B:** *"Se reportan las cuatro cifras, con la k dicha en
voz alta, o no se ha reportado nada."* Las "cuatro cifras" son Recall@k y
nDCG@k de los dos modelos comparados — nunca una sola cifra suelta.

Y la versión incómoda: *"una sola cifra no es un resultado, es la cifra que
mejor le quedaba a quien escribió el informe."*

---

## 5. Qué sigue después de nuestro taller (contexto, no es lo que presentamos)

- **Taller C (grupos 1 y 2, 11:40):** la tercera decisión — contra qué
  línea base se compara. Introduce una cuarta cifra, **cobertura** (qué
  fracción del catálogo llega a recomendarse alguna vez), porque un modelo
  puede acertar mucho y enseñar muy poco catálogo (popularidad acierta 41 %
  pero solo llega a nombrar 10 de 111 ítems).
- **Reto 6** (se presenta al final del Taller C): ganarle a "repetir lo
  propio" sin encoger el catálogo — Recall@10 > 0.7100 **y** cobertura >
  0.50 a la vez. La corrida de referencia con el kNN por defecto da
  Recall@10 = 0.2613, así que arranca en "NO SUPERADO" a propósito.

Las tres reglas del sábado (A, B, C) dicen lo mismo con tres caras: **un
número sin contexto no es un resultado.** Hoy el contexto se llama partición,
k y línea base.
