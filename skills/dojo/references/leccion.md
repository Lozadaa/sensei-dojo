# La presentación de una kata

Un único archivo HTML sin dependencias externas, oscuro, que se abre en el navegador y
se navega con las flechas. Es lo que el aprendiz mira mientras tiene su herramienta
al lado.
Nadie lee paredes de texto: cada slide es una idea, un diagrama o una tarea.

## Contents · Índice

- La sala (índice)
- El mapa
- Diseño (no te salgas)
- Construirla
- Navegación (la plantilla la hace sola)
- Sensei (el compañero de la kata)
- Receta de slides (máximo 8)
- Reglas de texto
- Diagramas (inline SVG)
- Bloques especiales de la plantilla
- Abrir
- Canal web (la kata se dirige desde la presentación)

## La sala (índice)

`.dojo/lessons/index.html` es la portada del dojo: lista las katas con el mismo diseño,
para que la raíz del servidor nunca muestre un listado crudo de archivos.

- Si no existe, copia `assets/index.html` y sustituye `{{DOMINIO}}` (p. ej.
  `Git · control de versiones`) y `{{CINTURON}}` (p. ej. `Cinturón blanco`).
- La plantilla ya trae el Sensei (mini en la marca, grande en la cabecera).
- Cada vez que creas una lección, inserta una fila justo después de `<!-- KATAS -->`
  (la más reciente arriba):
  ```html
  <a class="row" data-id="G-W1" href="001-repo-por-dentro.html"><span class="n">01</span><span class="t">Tu repo, por dentro</span><span class="d">2026-10-18</span></a>
  ```
  `data-id` es el id del concepto en PROGRESS.md: `refresh.py` marca la fila `data-done="1"`
  (cara contenta) cuando está practicado o dominado. Pásalo tras GUARDAR.
- Al subir de cinturón, actualiza la línea `class="belt"`.
- Si no hay katas todavía, deja `<div class="empty">Tu primera kata aparecerá aquí.</div>`.
- Bajo el saludo, una línea gris con la primera frase de «por qué estás aquí»
  (`<p class="porque"><!-- PORQUE --></p>`, la rellena `scripts/mapa.py`), y junto a
  «Continuar» el botón «Ver el mapa» (tecla M).

## El mapa

`.dojo/lessons/mapa.html` lo genera `scripts/mapa.py` (lo llama `refresh.py` siempre al
final; `--saludo` no le afecta). No lo edites a mano: se rehace en cada GUARDAR.

- **Qué lee**: el curriculum (`### ID Título            prereq: A, B`), PROGRESS.md,
  REFUERZO.md (lagunas `abierta…`), DUDAS.md (acción `profundizar…`, `gancho…` sin
  `resuelta`), DOJO.md (`Meta a 3 meses` y `Meta → conceptos`) y las filas de la sala.
- **Qué calcula**: el concepto actual (la kata más reciente con su concepto visto o
  practicado; si no hay, el primero cuyos prerrequisitos estén dominados), el camino a la
  meta (cierre de prerrequisitos de las anclas, sin lo dominado, en orden de cinturón) y
  tres frases: por qué estás aquí, cuánto falta para la meta, qué te debe el dojo.
- **Cómo se lee** (árbol de habilidades): crece hacia arriba desde la raíz; cada concepto
  está en la fila de su profundidad de prerrequisitos y bajo sus padres, unidos por conectores
  en codo. Cada gema pixel lleva un glifo: candado = bloqueado, + = disponible (sus
  prerrequisitos están dominados), anillo = visto, puntos = practicado, ✓ papel = dominado,
  bermellón = estás aquí (con el Sensei encima). Borde bermellón = camino a tu meta; anillo
  discontinuo y «META» = ancla de la meta; «L#» = laguna; «?» = duda por profundizar.
  Pasar por una gema enseña su ficha; clic abre su kata; Esc vuelve a la sala.
- Sin `Meta → conceptos` el mapa lo dice en la segunda frase: fíjala.

## Diseño (no te salgas)

- **Rejilla.** Columna centrada = canal (64 px) + medida (880 px); tres líneas: canal
  (números de `ol`, el Sensei junto a cada `h2`), eje (títulos, párrafos, texto de listas,
  cajas, `.grade`, `.said`, botones, diagramas, puntos) y borde derecho (cinturón,
  contador). Texto y formularios miden `--measure` (640 px). El contenido empieza
  siempre en la misma línea T (192 px a 1000 de alto), nunca centrado. En tarjetas y
  columnas, el eje es el de su pregunta o columna.
- **Ritmo de 8 px.** Etiqueta → título 8, título → cuerpo 24, entre bloques 32. No
  añadas márgenes sueltos en los slides.
- **Escala (6 tamaños).** 64 · 40 · 28 · 18 · 14 · 12: serif 64 (portada), 40 (`h2`),
  12 versalitas (`h3`, etiquetas); sans 28 (`lead`, pregunta), 18 (cuerpo), 14 (botones,
  bocadillo, historial, notas de diagrama). `code` mono al tamaño del texto. Nada más.
- **Diagramas.** `svg.dg` se pinta a su tamaño natural (1 unidad del viewBox = 1 px):
  viewBox de ancho ≤ 880, todo en la rejilla de 8 y empezando en x = 0 (si no, el
  diagrama no cae en el eje). Cajas de 48 de alto con 16 entre ellas, trazo de 1 px con
  coordenadas en .5, sin `rx`. Clases: `box` (`hot`, `ghost`), `lbl` (14, centrada), `l`
  (alineada a la izquierda), `path` (mono, para rutas), `note` (14, tenue), `hd`
  (etiqueta de columna, `hot`), `ln` (`hot`, `dash`), `frame`.
- **Comprobar.** Abre la kata y ejecuta `dojoGrid()` en la consola: debe devolver `[]`.

## Construirla

1. Copia `assets/plantilla.html` a `.dojo/lessons/NNN-slug.html`.
2. Sustituye `{{KATA}}` (p. ej. `Kata 03`), `{{TITULO}}` y `{{CINTURON}}`.
3. Sustituye el comentario `<!-- SLIDES -->` por tus `<section class="slide">`.
4. Ábrela (ver § Abrir).

No edites la plantilla original. No añadas fuentes ni scripts externos: tiene que
funcionar sin red y en cualquier navegador.

Si la plantilla cambia, `python scripts/refresh.py .dojo/lessons` reinyecta el
`<main id="deck">` de cada kata existente en la plantilla nueva y regenera `index.html`
sin tocar su contenido (añade el Sensei a las portadas que no lo tengan).

## Navegación (la plantilla la hace sola)

- Flechas ‹ › fijas a media altura (abajo, junto a los puntos, por debajo de 760 px).
  En el primer y último slide la flecha correspondiente queda atenuada.
- Puntos abajo desde el eje, clicables; los vistos en gris, el actual en acento.
  Contador `01 / 09` al borde derecho de la columna en pantallas anchas.
- Teclado: →, espacio, PageDown avanzan; ←, PageUp retroceden; Home, End. La flecha
  se ilumina ~180 ms al usar el teclado. `Esc` o la marca de arriba vuelven a la sala.
- **Hacer clic en el contenido no avanza.** No lo añadas: el aprendiz lo rechazó.
- `#N` en la URL abre el slide N y se actualiza sin llenar el historial.

## Sensei (el compañero de la kata)

Ninja pixel 24×24 dibujado en `<canvas>`, con la paleta del dojo. Sigue el ratón con
la mirada, parpadea y se balancea (quieto con `prefers-reduced-motion`). Se ve a
escala entera de píxel: 24 px en la marca, 48 junto a los títulos y 144 grande. No es decoración: habla,
da pistas, se inquieta si te atascas y celebra.

- Mini: ya está en la marca de la plantilla y del índice. No lo quites.
- Grande: `<canvas class="sensei big" width="24" height="24"></canvas>` como primer
  hijo de cada `section.cover` (portada y cierre).
- En el canal (lo pone la plantilla): 48 px junto al `h2` de cada slide que empieza con
  `h2` (no en portadas ni `split`), con el capuchón en el borde del canal; su bocadillo
  sale encima del título, sin tapar contenido. Mira abajo en Haz y en slides con
  diagrama. Cara de 24 px en cada `.grade` y en cada fila del índice; 48 px en `.said`.
- **Escribiendo** (lo pone la plantilla): mientras corrige una respuesta, contesta un mensaje
  o una petición de ayuda y prepara la siguiente kata (también "Continuar" en la sala), el
  Sensei toma la pose `write` (pincel que sube y baja, mirada al papel) con un bocadillo fijo
  "Escribiendo" y tres puntos; dura al menos 3 s (una página entera de tinta) aunque tu respuesta llegue antes.
- Humores (`data-mood`): `normal`; `point` en `do` (señala; también al abrirse el cierre);
  `focused` en `prove`, `think` mientras hay respuestas sin corregir o espera la siguiente
  kata, `happy` con total ≥ 5/6; `happy` en el último slide y al pasar por una kata en el
  índice; `surprised` 1,4 s al pulsar Revelar; `sleepy` en el índice cuando el saludo
  empieza por "Llevas". `data-mood` en una `<section>` fuerza su humor.

**Habla (`data-say`).** Cada `section.slide` lleva `data-say="…"`: lo que dice el Sensei
en un bocadillo al entrar. Todo bocadillo dura según su texto, max(8 s, 2 s + 80 ms por
carácter); con el ratón encima no se cierra y un clic lo cierra. Una línea de ≤ 60 caracteres, en
el idioma del aprendiz, con voz de sensei: breve, cálida, sin exclamaciones, sin
repetir el título del slide. Si falta, dice la frase de su tipo (portada "Vamos.",
Recuerda "Intenta antes de revelar.", Haz "Tu turno. Yo espero.", Demuestra "Aquí no
hay pistas.", cierre "Bien hecho."); `data-say=""` lo calla. Al revelar dice "¿Lo tenías?".

**Pistas (`data-hints`), solo en Haz.** `data-hints="pista 1|pista 2|pista 3"`: cada toque
al Sensei da la siguiente ("Pista 1 de 3 · …"); agotadas, un toque relee la última y el siguiente ofrece el botón
"Pedir ayuda al sensei" y "Tengo una duda" (abre el panel de dudas, § Canal web). Son
los peldaños 1-3 de la escalera de `pedagogia.md`: dónde mirar, qué buscar, casi la
respuesta. **Nunca la respuesta y nunca en Demuestra.** Fuera de Haz, tocarlo repite lo último que dijo en ese slide (o da ánimo si no dijo nada).

**Mirada.** Nunca sigue el ratón al píxel: se fija en él con retardo cuando se ha movido lejos,
lo mira un par de segundos y vuelve al frente; con el ratón quieto tiene miradas propias; mira
la caja donde escribes y al frente cuando habla. Todas las caras comparten la misma atención.

**Solo, sin configurar.** En Haz, a los 45 s sin tecla ni clic mira a los lados y dice
"¿Atascado? Tócame." una vez; 3 min después vuelve a mirar, callado (`?idle=N` en la
URL acorta el plazo para probar). En el cierre hace una reverencia.

**Saludo del índice (`{{SALUDO}}`).** Una línea bajo el título que el Sensei dice al
abrir la sala. Se elige en este orden y se escribe con
`python scripts/refresh.py .dojo/lessons --saludo "…"`:
- Última entrada en JOURNAL hace > 7 días: "Llevas N días sin venir. Empezamos suave."
- Racha ≥ 2 días: "Racha: N días."
- Acaba de subir de cinturón: "Cinturón X, nuevo."
- Si no: "Siguiente: <título de la próxima kata>."

## Receta de slides (máximo 8)

| # | Slide | Clase extra | Contenido | Límite |
|---|---|---|---|---|
| 1 | Portada | `cover` | Kata, título, una frase: qué vas a poder hacer al acabar | 20 palabras |
| 1b | Recuerda | — (la clase `recall` va solo en el `div` interior, nunca en la `section`) | Hasta 3 tarjetas: pregunta arriba, botón Revelar, respuesta oculta. Salen de REFUERZO.md (lagunas abiertas) y de los repasos vencidos de PROGRESS.md. Se omite si no hay nada | 3 tarjetas |
| 2 | Dónde estamos | — | Mini-mapa de la herramienta o de sus piezas con lo de hoy marcado en acento | diagrama + 1 línea |
| 3 | La idea | — | El concepto en una frase grande + diagrama que lo muestra funcionando | 30 palabras |
| 4 | Lado a lado | `split` | Las dos formas del mismo concepto en el dominio (CLI / GUI, código / editor visual, consulta / resultado), mismas etiquetas. Se omite si el dominio solo tiene una forma | 8 líneas por lado |
| 5 | Predice (opcional) | — | Pregunta "¿qué pasará si...?" con botón que revela la respuesta | 25 palabras |
| 6 | HAZ | `do` (con código: `do split`) | Tarea en la herramienta, pasos numerados, cada paso una línea. Si hay más de una línea de código, `do split`: pasos a la izquierda, código a la derecha (§ Bloques especiales) | ≤ 8 pasos |
| 7 | DEMUESTRA | `prove` | Las 3 preguntas, sin respuestas (las respuestas están solo en tu curriculum). Se responden en el propio slide: no escribas "responde en el chat". **Una pregunta por vez: la plantilla lo hace sola** (ver § Bloques especiales). Si la respuesta es código, `<li data-code="sh">` (o `py`, `js`, `sql`, `cs`, `cpp`, `ini`, `txt`) | 3 preguntas |
| 8 | Cierre | `cover` | "Ya puedes…" + gancho para la próxima | 2 líneas |

Para `/dojo explica <tema>`: slides 3, 4 (o un diagrama) y un cierre. Tres slides.
Para modo reparar: slides 3 con otro formato, 6 reducido a 3 pasos, 7 con una pregunta.

## Reglas de texto

- **Solo se pregunta lo que un slide explicó.** Cada pregunta de Demuestra apunta a una
  frase explícita de un slide anterior (La idea, Lado a lado o Predice). Lo que solo aparece de
  paso en un diagrama, en el código del Haz o en una nota no se pregunta: el aprendiz lo vive
  como trampa ("estás preguntando cosas que no has explicado"). Si una pregunta del
  curriculum no tiene su frase, añade la frase o cambia la pregunta.

- **Haz con mapa.** Si la tarea toca 3 o más piezas (funciones, archivos, los dos lados
  de una herramienta), el slide Haz lleva, entre el título y los pasos, un diagrama pequeño
  (≤ 128 px de alto) con qué llama a qué y en qué paso se hace cada cosa. Sin él, el
  aprendiz lo dijo así: "el código en cada punto se entiende poco y su relación también".
- Un título por slide, de 2 a 6 palabras.
- Cuerpo: frases cortas. Nada de párrafos de más de 2 líneas.
- Términos de la herramienta tal como aparecen en ella (`git status`, `HEAD`, `Staged
  Changes`); la explicación en el idioma del aprendiz.
- Código: bloques `<pre><code>` de máximo 8 líneas, resaltando con `<b>` solo la línea
  que importa.
- Las teclas van en `<kbd>`.

## Diagramas (inline SVG)

Todo diagrama es un `<svg class="dg" viewBox="0 0 720 300">` dentro del slide. Usa solo
estas clases, que la plantilla ya estiliza en oscuro:

- `.box` rectángulo (fill papel tenue, stroke tinta), `.box.hot` el de hoy (stroke
  acento, fill acento tenue).
- `.lbl` texto dentro de una caja; `.note` texto pequeño apagado.
- `.ln` línea o flecha (stroke tinta), `.ln.hot` en acento. Flechas con
  `marker-end="url(#arrow)"`; el marker ya existe en la plantilla.

Tipos que funcionan:

- **Flujo**: cajas en fila con flechas. Para ciclos de vida, orden de llamadas,
  compilación.
- **Mapa de piezas**: cajas apiladas con una columna "local / remoto / ambos" (o lo que
  separe el dominio). Para el sistema del cinturón naranja.
- **Dónde en la herramienta**: un rectángulo grande con sus zonas dentro (en un IDE:
  explorador, editor, terminal, control de código) y la de hoy en `.hot`.
- **Antes / después**: dos cajas con el mismo contenido y la diferencia en acento.

Dibuja de verdad el mecanismo. Un diagrama de tres cajas genéricas "Input → Proceso →
Output" no enseña nada; uno con `working tree → staging → commit → remoto` con la
caja de hoy en acento sí.

Ejemplo de flujo:

```html
<svg class="dg" viewBox="0 0 720 160">
  <rect class="box" x="10" y="50" width="150" height="60" rx="4"/>
  <text class="lbl" x="85" y="86">Working tree</text>
  <line class="ln" x1="160" y1="80" x2="200" y2="80" marker-end="url(#arrow)"/>
  <rect class="box hot" x="200" y="50" width="150" height="60" rx="4"/>
  <text class="lbl" x="275" y="86">Staging</text>
  <line class="ln" x1="350" y1="80" x2="390" y2="80" marker-end="url(#arrow)"/>
  <rect class="box" x="390" y="50" width="150" height="60" rx="4"/>
  <text class="lbl" x="465" y="86">Commit</text>
  <line class="ln" x1="540" y1="80" x2="580" y2="80" marker-end="url(#arrow)"/>
  <rect class="box" x="580" y="50" width="130" height="60" rx="4"/>
  <text class="lbl" x="645" y="86">Remoto</text>
  <text class="note" x="275" y="135">hoy: git add elige qué entra</text>
</svg>
```

## Bloques especiales de la plantilla

- **Haz con código (`do split`).** Si hay más de una línea de código, el Haz se divide:
  `<section class="slide do split">` con, en orden, `<h2>Haz</h2>`, el `<svg class="dg">`
  opcional (mapa, a todo el ancho), `<div><ol class="steps">…</ol></div>` (izquierda) y
  `<div class="code">` (derecha) con una `<figure><figcaption>Archivo · pasos 1-3</figcaption>
  <pre data-code="py"><code>…</code></pre></figure>` por archivo (`py`, `js`, `sql`, `sh`, `cs`,
  `cpp`, `ini`, `txt`;
  coloreado y sin scroll horizontal). **Nunca bloques de código dentro de los pasos**: en ellos
  solo identificadores en `<code>` y teclas en `<kbd>`. `<li data-lines="3-5">` resalta esas
  líneas de la primera figura al pasar por el paso (`"2:1-4"`, de la segunda). Por debajo de
  1280 px se apila: pasos arriba, código abajo.

- Predice: `<h3>Predice</h3>`, `<p class="lead">…?</p>`,
  `<button class="reveal" data-target="r1">Revelar</button>` y
  `<p id="r1" class="hidden">…</p>`, todo como hijos directos de la `section`: así
  quedan en un mismo eje y la respuesta mide lo mismo que la pregunta. El icono del
  botón lo pone la plantilla; no escribas flechas en el texto.
- **Una pregunta por vez (Demuestra y Recuerda).** Escribe las 3 preguntas o tarjetas como
  siempre; la plantilla enseña solo la activa ("Pregunta 1 de 3", texto en lead, caja y
  Enviar). Al corregirse (o revelarse la tarjeta) aparece "Siguiente pregunta" y **solo ese
  botón avanza** (nunca pasa sola; el aprendiz lo pidió); la hecha se pliega arriba a una
  línea ("01 · 2 / 2 · pregunta"). En la última de Demuestra el botón es "Ver el total"; la
  última de Recuerda se queda abierta. Cada `grade` tiene su reacción: 2/2 pulso bermellón,
  reverencia del Sensei y los puntos parpadean; 1/2 pulso corto;
  0/2 sin pulso y una frase que acompaña. Al recargar se rehace el historial desde las
  `grade` sin animaciones. Sin servidor, el botón dice "Responde en el chat" y pasa a la
  siguiente.
- **Cajas de código (`data-code`).** En una pregunta de Demuestra o una tarjeta de Recuerda
  cuya respuesta es código, `data-code="py"` (`js`, `sql`, `sh`, `cs`, `cpp`, `ini`, `txt`) cambia la caja por un
  editor monoespaciado (3 líneas vacío, crece hasta 16), con tabulador de dos espacios y
  coloreado en vivo (sin librerías), y el botón debajo a la derecha. Enviada o corregida
  muestra el código entero con sangría colgante; solo el historial lo pliega a su primera línea.
- Recuerda (recuerdo activo): el aprendiz intenta responder de memoria, revela y se
  comprueba solo. Cada tarjeta lleva un `tag` con el origen (laguna o repaso) y la
  respuesta sí va en el HTML, porque aquí el objetivo es recordar, no examinar. El
  examen sigue siendo en el chat: tras el slide, pregunta en el chat UNA de las
  tarjetas sin avisar cuál; esa respuesta es la que puntúa.
  ```html
  <section class="slide">
    <h3>Recuerda</h3>
    <div class="recall">
      <div>
        <span class="tag">laguna · kata 03</span>
        <p>¿Qué tecla cierra <code>git log</code>?</p>
        <button class="reveal" data-target="c1">Revelar</button>
        <p id="c1" class="hidden"><kbd>q</kbd>. <code>git log</code> abre un paginador; <kbd>Esc</kbd> no lo cierra.</p>
      </div>
    </div>
  </section>
  ```
- Pasos: `<ol class="steps"><li>…</li></ol>`.
- Preguntas: `<ol class="qs"><li>…</li></ol>`.
- Lado a lado: `<section class="slide split"><div><h3>Forma A</h3>…</div><div><h3>Forma B</h3>…</div></section>` (p. ej. CLI / GUI).
  Dos columnas iguales hasta 1280 px, apiladas por debajo de 760 px. El código nunca
  hace scroll horizontal: si una línea no cabe, continúa con sangría bajo su nivel.
  Un `<b>` no debe cruzar saltos de línea dentro del `<pre>`.

## Abrir

1. Sirve la carpeta de lecciones con `scripts/serve.py` (no con `python -m http.server`:
   ese no recibe las señales de los botones). Si `http://localhost:8766/` ya responde,
   no arranques otro. Si no, en segundo plano (Bash con `run_in_background`):
   ```bash
   python "<skill>/scripts/serve.py" .dojo/lessons --port 8766
   ```
   Si el puerto está ocupado por un `http.server` viejo, páralo antes. Con el navegador
   integrado puedes usar `preview_start` con esta entrada en `.claude/launch.json` del
   proyecto (el panel no abre `file://`):
   ```json
   { "name": "dojo", "runtimeExecutable": "python",
     "runtimeArgs": ["<skill>/scripts/serve.py", ".dojo/lessons", "--port", "8766"],
     "port": 8766 }
   ```
   y `navigate` a `http://localhost:8766/NNN-slug.html`. Si `preview_start` arranca otra
   configuración (la app a veces cachea un launch.json anterior), páralo y usa el
   arranque en segundo plano.
2. Si no hay forma de servir por HTTP, abre con el sistema: Windows `start "" "<ruta>"`,
   macOS `open "<ruta>"`, Linux `xdg-open "<ruta>"`. Los botones dirán "Escribe /dojo
   en el chat" y las cajas "Responde en el chat": el aprendiz te avisa a mano.
3. Dile al aprendiz en una línea que está abierta y cómo avanzar (flechas ‹ › o →).
   Puedes mandarle a un slide concreto con `#N` en la URL.
4. Haz visible el panel: `mcp__ccd_view__show_pane` con `pane: "preview"` (en la app
   de escritorio el panel puede estar oculto aunque la pestaña exista). Si el aprendiz
   sigue sin verla, ábrela también en su navegador del sistema: en Windows
   `Start-Process "<url>"` desde PowerShell (`cmd /c start` desde Bash no abre nada),
   en macOS `open "<url>"`. No le hagas pedirlo dos veces.

Si la presentación falla al abrir, no la describas en el chat: arréglala y vuelve a
abrir. El chat sigue siendo de 6 líneas máximo.

## Canal web (la kata se dirige desde la presentación)

Con `serve.py` corriendo, el aprendiz no vuelve al chat en todo el ciclo: responde, pide
ayuda y pasa a la siguiente kata desde la página. La plantilla pone sola botones y
formularios; no los escribas en los slides. Dos archivos append-only en `.dojo/`:

- `signals.jsonl`: lo que manda la página (`POST /signal`); lo escribe `serve.py`.
- `feedback.jsonl`: lo que respondes tú; la página lo lee con `GET /feedback?since=N`
  cada 5 s en reposo, 3 s en Haz y Recuerda, 1,5 s mientras espera una corrección o la
  siguiente kata. Nunca lo edites ni
  lo vacíes: la página cuenta líneas.

### Señales que llegan

```json
{"ts": "2026-10-18T21:05:12-03:00", "type": "answer", "kata": "001-proyecto-y-carpetas", "slide": 8, "q": 2, "text": "Binaries, Intermediate y Saved"}
```

| `type` | De dónde | Campos | Tu respuesta en feedback.jsonl |
|---|---|---|---|
| `answer` | caja bajo cada pregunta de Demuestra | `slide`, `q` (1..3), `text` | `grade` en cuanto llega, sin esperar las otras |
| `recall` | caja de cada tarjeta de Recuerda | `slide`, `q` (tarjeta), `text` | `grade` (la tarjeta de REFUERZO se cierra o sigue abierta) |
| `message` | botón "Tengo una duda" (abajo a la izquierda, tecla ? o D) en cualquier slide y en la sala (`kata: "index"`) | `slide`, `text` | `say` con `"channel": "duda"`, ≤ 140 caracteres con la `kata` del mensaje (sale en el panel de dudas y en el slide); "cansado" → `end`. Si la duda abre un tema de otro cinturón, respóndela corta y anótala en JOURNAL como curiosidad pendiente |
| `help` | bocadillo tras agotar `data-hints` | `extra.pistas` | `say` con `"channel": "duda"` y el peldaño 4 (la respuesta y por qué); puntúa 0 y va a REFUERZO |
| `done` | "Ya lo hice" en Haz | — | `say` que invita a Demuestra (si la key trae `done`, ya lo escribió `serve.py`: la señal llega con `handled`) |
| `next` | "Siguiente kata" en el cierre | — | GUARDAR, construir la siguiente kata (o el repaso que toque) y `next_ready` |
| `continue` | "Continuar" en la sala | `kata` = la última | Igual que `next`: decide el MODO, construye y `next_ready` |

Todas llevan `ts` y `kata` (nombre del archivo sin `.html`); `slide` es 1-based.

### Lo que escribes

Una línea JSON por mensaje, añadida al final (`>>`), `text` ≤ 140 caracteres, sin
emojis, con la voz del Sensei. `kata` es la de la señal que contestas.

```json
{"ts": "…", "type": "grade", "kata": "001-repo-por-dentro", "slide": 8, "q": 2, "score": 2, "text": "Exacto: todo el historial vive en .git.", "mood": "happy"}
{"ts": "…", "type": "say", "kata": "001-repo-por-dentro", "text": "Bien. Ahora, Demuestra: responde ahí mismo.", "mood": "normal"}
{"ts": "…", "type": "next_ready", "url": "002-tu-primer-commit.html", "title": "Kata 02 · Tu primer commit"}
{"ts": "…", "type": "end", "text": "Por hoy, basta. Ya sabes qué guarda Git y dónde."}
```

- `grade`: copia `slide` y `q` de la señal (sin `slide`, la página usa la caja que
  espera corrección con esa `q`). `score` 0/1/2 según SKILL.md § Cómo leer respuestas; `text` dice por qué
  (si es 0 o 1, la respuesta correcta en pocas palabras). `mood` opcional: happy,
  focused, surprised o normal. La página la pinta bajo la pregunta ("2 / 2") y el
  Sensei reacciona. Una respuesta parcial no se repregunta: puntúa 1 y corrige.
- `say`: lo dice el Sensei en el bocadillo (8 s) y queda escrito en el slide actual.
  `kata: "index"` (o sin `kata`) para la sala. `channel` opcional: `"duda"` lo manda solo al
  panel "Tengo una duda" (historial y punto bermellón), nunca al bocadillo ni al slide; sin
  `channel` (o `"slide"`), al slide como siempre. Las respuestas a `message` y `help` van con
  `"channel": "duda"`.
- `next_ready`: `url` relativa a `lessons/` (`NNN-slug.html`, nada más), `title` corto.
  Vale para cualquier página abierta: la sala o la kata navegan solas a los 1,2 s.
- `end`: cierra la sesión con victoria (cansado, dos ceros seguidos, prisa). La página
  muestra el texto y "Volver a la sala". Guarda antes de escribirla.

Escribe con un heredoc o `printf '%s\n' '{…}' >> .dojo/feedback.jsonl`; comprueba que es
JSON válido de una línea (una línea rota llega como `null` y se ignora).

### Hoja de respuestas (la IA solo cuando hace falta)

Junto a cada kata, `lessons/NNN-slug.key.json` (misma base que el HTML; `serve.py` nunca
la sirve). Claves `"slide:q"`, como en las señales:

```json
{"kata": "004-deshacer-sin-miedo", "next": "005-ramas.html",
 "questions": {"7:1": {
   "full":    [{"match": "re:\\brestore\\b[\\s\\S]*--staged", "text": "git restore --staged: saca el archivo de staging sin tocar tu cambio.", "mood": "happy"},
               {"match": "git restore --staged"}],
   "partial": [{"match": "re:^\\s*(git\\s+)?restore\\s*$", "text": "restore sí; con --staged lo sacas de staging y el cambio se queda.", "mood": "focused"}],
   "wrong":   {"text": "git restore --staged <archivo>: deshace el add, no el cambio.", "mood": "surprised"}}},
 "recall": {"2:1": {"full": [{"match": "re:^\\W*q\\W*$", "text": "q cierra el paginador."}]}}}
```

- `match` de texto: igual a la respuesta sin mayúsculas, sin acentos, con los espacios
  colapsados y sin puntuación final (`"git add"` casa con `"Git add."`). `re:` es una regex
  sin mayúsculas, que se prueba con la respuesta tal cual y normalizada; en JSON las `\`
  van dobles. Usa regex para variantes: `re:^\W*(la\s+)?(tecla\s+)?f\W*$` (F, la f, tecla
  F), `re:\b(ctrl|control)\s*[+-]?\s*shift\s*[+-]?\s*s\b` (con o sin espacios),
  `re:src[\\/]+app` (rutas con / o \). Para excluir trampas, una negativa al inicio:
  `re:^(?![\s\S]*--hard)[\s\S]*\breset\b`.
- Orden: `full` (2) → `partial` (1) → si nada casa y `wrong` lleva `"auto": true`, 0 con su
  texto. Si no, la respuesta va a la IA como siempre. Una regla sin `text` usa el de la
  primera de su grupo. `mood` por defecto: happy, focused, surprised.
- `serve.py` escribe la grade con `"by": "key"` y anota la señal con `"graded": "key"`.
- `"done": {"text": "…≤ 140", "mood": "point"}` (opcional, nivel superior; mood por defecto
  `point`): el "Ya lo hice" recibe ese `say` al instante y la señal lleva `"handled": "key"`.
  Sin `done`, lo respondes tú. `help` y `message` van siempre a la IA.
- `"next"`: si ese archivo existe, `next` recibe `next_ready` al instante (`"by": "key"`) y
  la señal lleva `"handled": "key"`. `continue` igual, salvo que la kata esté a medias (no
  todas sus preguntas tienen grade): entonces la reabre. Tú sigues recibiendo la señal para
  GUARDAR y preparar la kata siguiente a esa.
- Escribe variantes de verdad: lo que el curriculum da por bueno, sinónimos, con y sin
  puntos o comillas, y la trampa típica como `partial`. Ante la duda, deja que lo vea la IA.
  Comprueba la lógica con `python scripts/serve.py --selfcheck`.

### Lo que ve el aprendiz

- **Demuestra**: bajo cada pregunta, caja cuyo alto marca el contenido (1 línea vacía,
  hasta 16; o el editor de código con `data-code`) y "Enviar" (también
  <kbd>Ctrl</kbd>+<kbd>Enter</kbd>). Enviada, conserva su alto y el botón dice
  "Corrigiendo" con un spinner pixel, el Sensei escribe (pose `write`) y el hueco de la nota
  muestra una línea que avanza, hasta que llega la `grade`. Tras cada corrección, "Siguiente pregunta";
  en la última, "Ver el total" enseña el total ("5 / 6", subrayado si es ≥ 5) y la flecha late.
- **Recuerda**: la misma caja ("De memoria") en cada tarjeta, antes de Revelar (que sigue disponible).
- **Cierre**: "Siguiente kata" está bloqueado ("Responde primero las tres") hasta tener
  las tres `grade`. Pulsado: "Preparando tu siguiente kata…", el Sensei concentrado y los
  puntos laten hasta `next_ready` o `end`. A los 3 min sin respuesta: "Parece que el
  sensei no está. Escribe /dojo en el chat."
- **Sala**: "Continuar" espera igual.
- **Sin servidor** (estático o `file://`): las cajas dicen "Responde en el chat", los
  botones "Escribe /dojo en el chat", y el cierre no se bloquea.

Al recargar, la página repinta las `grade` de su kata; los `say`, `next_ready` y `end`
anteriores a abrirla no se repiten.

### Vigilante

En MOSTRAR, justo después de abrir la presentación (o la sala al invocar), arma Monitor:

```
Monitor  command: tail -n0 -F .dojo/signals.jsonl
         description: "señales del dojo"   timeout_ms: 1800000
```

Cada línea es una señal: contesta según la tabla escribiendo en `feedback.jsonl`, sin
esperar mensajes del chat y sin escribir en el chat más que una línea de estado si hace
falta. Al expirar, lee las líneas con `ts` posterior a la última atendida, atiéndelas y
rearma, mientras haya una kata o la sala abierta. Si no hay Monitor, el aprendiz escribirá
en el chat.

**Al invocar `/dojo`.** Arranca `serve.py` si no responde, arma el Monitor y abre la sala:
ella dirige. Antes, lee `signals.jsonl`: son pendientes las líneas con `ts` posterior a la
marca `Señales hasta: <ts>` de la última entrada de JOURNAL (sin marca, las de fecha
posterior a esa entrada); atiéndelas en orden (un `answer` sin `grade` se corrige ya, un
`next` sin `next_ready` se prepara ya). Al guardar, escribe en JOURNAL `Señales hasta:
<ts>` con la última que atendiste.
