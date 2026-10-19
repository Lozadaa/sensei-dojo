# Curriculum para un dominio nuevo

Cada dojo tiene su curriculum en `.dojo/curriculum.md` (una web, una base de datos,
Git, Blender, un lenguaje, un motor de juego, un instrumento). El sensei lo crea en la
ceremonia de entrada; este archivo explica cómo construirlo bien. Al final hay un
concepto de ejemplo completo: copia su forma, no su contenido.

## Antes de escribir una línea

1. **Elige el proyecto base.** Todas las katas se hacen sobre la misma cosa
   determinista: una plantilla oficial, un repo de ejemplo, un dataset público, un
   archivo de muestra. Sin proyecto base no hay preguntas deterministas. Pregunta al
   aprendiz si ya tiene uno; si no, el primer concepto del primer cinturón es crearlo.
2. **Decide las dos formas** si el dominio las tiene (código / editor visual, CLI /
   GUI, fórmula / gráfico, teoría / instrumento). Si no las tiene, el slide "Lado a
   lado" no se usa.
3. **Nombra el sistema**: las 5-8 piezas que crean, poseen o llaman a las demás. Van
   en un cinturón intermedio, pero se mencionan desde el primero.
4. **Busca material técnico ya instalado**: skills, documentación local, manuales
   (`ls ~/.claude/skills`, carpetas `docs/` del proyecto). Son tu referencia para no
   inventar respuestas; nunca se cargan enteros en el chat del aprendiz.

## Cinturones

Siete, de blanco a negro, cada uno con 4-6 conceptos. Orden habitual:

| Cinturón | Qué cubre |
|---|---|
| Blanco | Orientación: la herramienta, el proyecto base, dónde está cada cosa, cómo ejecutar y parar |
| Amarillo | El dialecto: convenciones, archivos de configuración, cómo compilar o correr, cómo ver lo que pasa (logs, debug) |
| Naranja | El sistema: las piezas principales y cómo se hablan (eventos, llamadas, datos) |
| Verde | Lo visible: salida, interfaz, presentación, datos externos |
| Azul | Comportamiento avanzado del dominio (animación, concurrencia, consultas complejas, lo que corresponda) |
| Marrón | Sistemas transversales: persistencia, arquitectura de datos, organización a escala |
| Negro | Red, rendimiento, distribución o lo que separe a un profesional |

Si el dominio es más pequeño, menos cinturones, nunca menos de tres. El aprendiz no
necesita ver todos los cinturones el primer día: PROGRESS.md solo lista el actual.

## Formato de cada concepto

El encabezado `### <ID> <nombre>            prereq: <ids>` es obligatorio tal cual (ID con
guion, p. ej. `B-W1`; `prereq: —` si no depende de nada; varios separados por comas) y
cada cinturón empieza con `## Cinturón <color> · <título>`: de ahí sale el mapa.

```
### <ID> <nombre>            prereq: <ids>
Por qué: una línea que conecte con la meta a 3 meses del aprendiz.
Kata (≤7 pasos): la tarea en la herramienta real, sobre el proyecto base.
Diagrama: qué dibujar (flujo, mapa de piezas, dónde-en-la-herramienta, antes/después).
Lado a lado: qué comparar, o "no aplica".
Preguntas (Q → R esperada): tres o más deterministas; elige 3 por kata.
Trampas: errores típicos y cómo nombrarlos sin juzgar.
```

ID = inicial del dominio + inicial del cinturón + número (`W-W1`, `S-Y3`).

Ejemplo completo (Git):

```
## Cinturón blanco · El repo y el primer commit

### G-W2 Tu primer commit            prereq: G-W1
Por qué: sin commits no hay historial que recuperar ni compartir.
Kata (≤7 pasos): en el repo de práctica, crea notas.txt, mira git status, git add
  notas.txt, vuelve a mirar git status, git commit -m "primera nota", git log --oneline.
Diagrama: flujo working tree → staging → commit, con staging en acento.
Lado a lado: terminal / panel de control de código del editor, mismas etiquetas.
Preguntas (Q → R esperada):
  - ¿Qué comando pasa notas.txt a staging? → git add notas.txt
  - ¿Qué palabra usa git status para lo que está en staging? → Changes to be committed
  - ¿Un archivo tras git add ya está en el historial? → No: entra con git commit
Trampas: creer que add guarda (nómbralo: "add elige, commit guarda"); olvidar -m y
  quedar dentro del editor de texto.
```

## Preguntas deterministas: qué vale y qué no

Vale todo lo que tiene una sola respuesta comprobable que el aprendiz solo sabe si
hizo la tarea:

- el nombre exacto de un panel, menú, comando, atajo, archivo, carpeta, función,
  macro, clase, opción;
- un valor por defecto que aparece en pantalla;
- el texto literal de un mensaje, error o línea de salida ("pega la línea…");
- qué pasa (un hecho observable) al hacer X: "¿el cambio persiste al parar?";
- una captura de pantalla de un lugar concreto (el sensei la lee).

No vale: "¿qué te pareció?", "explica con tus palabras" como prueba (solo como
cierre), cifras que cambian entre versiones sin pedir que pegue el texto, nada que
el aprendiz pueda adivinar sin haberlo hecho.

Si una respuesta depende de la versión de la herramienta, pide el texto o la captura y
verifica estructura, no cifras.

## Diagnóstico

Una pregunta determinista por cinturón, de la más básica a la más avanzada, elegida
entre las de cada cinturón. El sensei para al segundo fallo seguido. Escríbelas en la
sección `## Diagnóstico` del curriculum antes que los cinturones.

## Crear el curriculum en la ceremonia

No se escribe entero el primer día: tres cinturones completos (blanco, amarillo,
naranja) y solo los títulos de los demás. Los siguientes se detallan al llegar, con lo
aprendido del aprendiz (su meta, sus malentendidos). Antes de darlo por bueno,
compruébalo contra la documentación local o los skills instalados: una respuesta
esperada equivocada en el curriculum es peor que una pregunta de menos.
