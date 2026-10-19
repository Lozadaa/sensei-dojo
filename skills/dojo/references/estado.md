# Estado persistente: formatos exactos

Todo vive en `.dojo/` del proyecto. Markdown plano para que el aprendiz pueda leerlo y
editarlo a mano. Fechas siempre absolutas AAAA-MM-DD.

## DOJO.md

```markdown
# DOJO · <Dominio>

- Creado: 2026-10-17
- Dominio: git               (el curriculum vive en .dojo/curriculum.md)
- Herramienta/versión: Git 2.x   (lo que diga el aprendiz; vacío si no lo sabe)
- Proyecto base: <Nombre>    (dónde se hacen las katas; p. ej. un repo de práctica en
                              Git, la app de ejemplo de un framework, una base de
                              datos de muestra en SQL)
- Idioma: es                (es o en: idioma de la interfaz de katas, sala y mapa;
                              el contenido lo escribes siempre en el idioma del aprendiz)

## Aprendiz
- Cinturón actual: blanco
- Meta a 3 meses: "<frase literal del aprendiz>"
- Meta → conceptos: G-O1, G-O4, …   (3-6 anclas del curriculum que cumplen la meta; las fija
  el sensei en la ceremonia o al revisar la meta. El mapa calcula el camino desde ellas)
- Base previa: nunca | lee | escribe   (el lenguaje o base del dominio: shell, JS, SQL…)
- Ritmo observado: normal
- Formatos que le funcionan: (vacío hasta observar)
- Energía típica: (vacío hasta observar)

## Reglas acordadas
- El sensei no escribe código salvo dictado.
- Kata de 15-20 min.
- (las que el aprendiz haya elegido; p. ej. "primero la terminal, luego la GUI")

## Malentendidos activos
- (ninguno)
```

## PROGRESS.md

Una fila por concepto del curriculum. Se crean todas las filas del cinturón actual al
entrar en él; los cinturones futuros se añaden al llegar.

```markdown
# Progreso

Cinturón: blanco · Katas: 0 · Racha: 0 días · Última kata: —

| id | concepto | estado | puntaje | pistas | repaso | intentos |
|---|---|---|---|---|---|---|
| G-W1 | El repo por dentro | nuevo | — | — | — | 0 |
| G-W2 | Tu primer commit | nuevo | — | — | — | 0 |
```

Estados y transiciones:

```
nuevo → visto        (se mostró la presentación)
visto → practicado   (completó HACER y respondió, puntaje < 5/6)
practicado → dominado (puntaje ≥ 5/6 en kata, o 2/2 en modo salto)
dominado → practicado (un 0 en repaso)
```

Columna `repaso`: fecha del próximo repaso. Regla espaciada:

```
dominado por primera vez  → +3 días
repaso acertado (2)       → +7 días, luego +21, luego +60
repaso con pista (1)      → +3 días
repaso fallado (0)        → +1 día y estado practicado
```

Cinturón nuevo cuando todos los conceptos del actual están `dominado`. Al subir, la
cabecera cambia y se añaden las filas del siguiente cinturón.

## JOURNAL.md

Append-only. Una entrada por sesión. Respuestas literales del aprendiz entre comillas:
son el material para adaptar.

```markdown
## 2026-10-17 · Kata 3 · G-W3 Leer el historial · 12 min

Modo: avanzar
Formato: diagrama + predice
Tarea: hecha (necesitó pista 2 para encontrar --oneline)

Preguntas:
1. ¿Qué opción muestra un commit por línea? → "--oneline" · 2
2. ¿Qué tecla cierra git log? → "Esc... no, q" · 2
3. ¿Un archivo tras git add ya está en el historial? → "sí, ya queda guardado" · 0
   Malentendido: cree que add guarda en el historial. Atacar con "predice" en la próxima.

Puntaje: 4/6 → practicado · repaso 2026-10-18
Victoria dicha: "ya lees el historial y sabes qué hizo cada commit".
Gancho: "la próxima: deshacer sin miedo".
Curiosidades pendientes: "¿cómo se trabaja con otros en el mismo repo?"
Señales hasta: 2026-10-17T19:42:10-03:00
```

`Señales hasta` es el `ts` de la última línea de `signals.jsonl` que atendiste (omítela si
no hubo señales); ver `leccion.md` § Señales.

Entrada mínima en `/dojo explica <tema>`:

```markdown
## 2026-10-18 · Explica · .gitignore · 5 min
3 slides. Sin puntaje. Preguntó: "¿.gitignore borra los archivos?" → no, solo deja de seguirlos.
```

## REFUERZO.md (lagunas)

Cada cosa que el aprendiz no supo queda aquí hasta que la recuerde dos veces en días
distintos. Es la fuente del slide "Recuerda" de cada kata.

```markdown
# Refuerzo

| id | fecha | concepto | lo que no supo | respuesta | dijo | aciertos | próxima | estado |
|---|---|---|---|---|---|---|---|---|
| L1 | 2026-10-17 | G-W3 | tecla para cerrar git log | q | "Esc" | 0 | 2026-10-18 | abierta |
| L2 | 2026-10-17 | G-W2 | git add no guarda en el historial | solo prepara; guarda el commit | "ya queda guardado" | 1 | 2026-10-21 | abierta |
```

Entra una fila cuando:

```
puntaje 0 en cualquier pregunta         → abierta, próxima = mañana
pista de peldaño 3 o 4 en HACER         → abierta, próxima = mañana
"no entiendo" / "no me acuerdo" literal → abierta, próxima = mañana
```

Sale (estado `cerrada`) cuando acumula 2 aciertos sin pista en días distintos. Un fallo
en una tarjeta ya abierta pone `aciertos` a 0 y `próxima` a mañana. Columna `dijo`:
respuesta literal del aprendiz; sirve para formular la tarjeta con su propio error.

Las lagunas cerradas se quedan en la tabla (son historia útil); nunca se borran.

## DUDAS.md (lo que preguntó dirige lo que viene)

Cada pregunta del aprendiz (botón "Tengo una duda", "Pedir ayuda", un "no entiendo" en
cualquier canal) y cada pista de peldaño 3 o 4 queda aquí con su frase literal y el
concepto al que apunta. No es un registro: es la lista de lo que hay que profundizar.

```markdown
# Dudas

| id | fecha | kata | concepto | dijo | respuesta corta | señal | acción |
|---|---|---|---|---|---|---|---|
| D1 | 2026-10-19 | 004 | G-Y1 | "¿si borro la rama pierdo los commits?" | no si ya están fusionados; si no, Git avisa | duda | resuelta |
| D2 | 2026-10-19 | 005 | G-O1 | "¿un rebase cambia los commits de los demás?" | solo reescribe los tuyos | adelantada | gancho en G-O1 |
| D3 | 2026-10-20 | 005 | G-Y2 | "sigo sin ver qué es HEAD separado" | HEAD apunta a un commit, no a una rama | no entiende | profundizar en kata 06 |
```

`señal`: `duda` (pregunta normal) · `no entiende` (lo dice o lo repite) · `pista 3-4` ·
`adelantada` (tema de un cinturón futuro) · `repite` (misma duda dos veces).
`acción`: `resuelta` · `profundizar en kata NN` · `gancho en <concepto>` · `tarjeta`
(va también a REFUERZO) · `explica` (mini-lección aparte).

Reglas al planificar la siguiente kata (MOSTRAR):
- Un concepto con 2 o más filas sin `resuelta`, o una sola con `no entiende` → la
  próxima kata abre con un slide "Profundiza" sobre ese concepto, con otro formato que
  el de la primera vez, y una pregunta determinista extra en Demuestra. Si además hubo
  un 0, es modo reparar.
- `adelantada` → se guarda como gancho: cuando llegue ese concepto, la kata empieza
  recordando su pregunta literal ("Esto lo preguntaste tú en la kata 05").
- `repite` → tarjeta en REFUERZO con la formulación exacta de la duda, y la key de la
  kata siguiente acepta esa formulación como variante.
- Tres dudas seguidas sobre cosas de otro cinturón → el aprendiz va más rápido que el
  plan: proponer salto con una pregunta por concepto.

## lessons/

`NNN-slug.html` con NNN = número de kata con tres cifras (`003-leer-el-historial.html`). La
presentación se conserva: el aprendiz puede reabrirla. Si una kata se repite en modo
reparar, el nuevo archivo es `003b-leer-el-historial.html`.

## signals.jsonl y feedback.jsonl (canal web)

Los crea el canal con la presentación (`leccion.md` § Canal web). Son append-only: nunca
los edites, vacíes ni reordenes; la página cuenta líneas de `feedback.jsonl`.

- `signals.jsonl`: lo escribe `serve.py` con cada botón o respuesta de la página. Es la
  fuente de las respuestas literales que copias a JOURNAL.
- `feedback.jsonl`: lo escribes tú, una línea JSON por corrección (`grade`), mensaje
  (`say`), lección lista (`next_ready`) o cierre (`end`).

## Al guardar

Orden: PROGRESS.md primero (es el que decide la próxima kata), luego REFUERZO.md
(lagunas nuevas y aciertos de las tarjetas), luego JOURNAL.md, luego DOJO.md solo si
cambió el perfil (cinturón, ritmo, formatos, malentendidos). Guardas antes del mensaje
de despedida, no después.
Con el canal web, la despedida es la línea `next_ready` o `end` de `feedback.jsonl`: guarda
antes de escribirla. En `next`/`continue` el orden es: guardar, actualizar el saludo del
índice (`refresh.py --saludo`), construir la siguiente kata, añadir su fila al índice y
escribir `next_ready`.
