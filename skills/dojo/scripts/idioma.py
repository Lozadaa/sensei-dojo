"""La interfaz en el idioma del aprendiz: la línea «- Idioma: xx» de DOJO.md.

Las plantillas de assets/ están en español. Para `en`, refresh.py y mapa.py pasan la plantilla
(nunca el contenido de la kata) por la tabla de abajo antes de inyectar el deck, y ponen
<html lang="en">. Otros idiomas se quedan en español hasta tener su tabla.
Comprobación: python scripts/idioma.py --selfcheck
"""
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

COMMON = [  # el panel «Tengo una duda» y la espera de la siguiente kata: igual en la kata y en la sala
    ("'Escribiendo'", "'Writing'"),
    ("'Enviar'", "'Send'"),
    ("'Vamos.'", "'Here we go.'"),
    ("'Vamos'", "'Here we go'"),
    ("'Escribe /dojo en el chat'", "'Type /dojo in the chat'"),
    ("'Preparando tu siguiente kata'", "'Preparing your next kata'"),
    ("'Parece que el sensei no está. Escribe /dojo en el chat.'", "'The sensei seems to be away. Type /dojo in the chat.'"),
    ("'Tengo una duda'", "'I have a question'"),
    ("'Escribe tu duda en el chat.'", "'Type your question in the chat.'"),
    ("'Pregunta al sensei (? o D)'", "'Ask the sensei (? or D)'"),
    ("'Pregunta al sensei'", "'Ask the sensei'"),
    ("'Cerrar (Esc)'", "'Close (Esc)'"),
    ("'Tu duda'", "'Your question'"),
    ("'Pregunta lo que no te cuadre de esta kata. Te respondo aquí.'", "'Ask anything in this kata that doesn’t add up. I’ll answer here.'"),
]

EN = {
    "plantilla.html": COMMON + [
        ('title="Tócame" aria-label="Sensei: tócame para una pista"', 'title="Touch me" aria-label="Sensei: touch me for a hint"'),
        ('title="Volver a la sala (Esc)"', 'title="Back to the dojo (Esc)"'),
        ('aria-label="Diapositivas"', 'aria-label="Slides"'),
        ('aria-label="Anterior" title="Anterior (←)"', 'aria-label="Previous" title="Previous (←)"'),
        ('aria-label="Siguiente" title="Siguiente (→)"', 'aria-label="Next" title="Next (→)"'),
        ("'Bien hecho.'", "'Well done.'"),
        ("'Intenta antes de revelar.'", "'Try before you reveal.'"),
        ("'Tu turno. Yo espero.'", "'Your turn. I’ll wait.'"),
        ("'Aquí no hay pistas.'", "'No hints here.'"),
        ("'Diapositiva '", "'Slide '"),
        ("'¿Lo tenías?'", "'Did you have it?'"),
        ("'Corrigiendo'", "'Grading'"),
        ("'Respuesta '", "'Answer '"),
        ("'Pega o escribe el código'", "'Paste or type the code'"),
        ("'Tu respuesta'", "'Your answer'"),
        ("'De memoria'", "'From memory'"),
        ("'en el chat'", "'in the chat'"),
        ("'Responde en el chat'", "'Answer in the chat'"),
        ("(s === prove ? 'Pregunta ' : 'Recuerda ') + (n + 1) + ' de ' + items.length",
         "(s === prove ? 'Question ' : 'Recall ') + (n + 1) + ' of ' + items.length"),
        ("'Ver el total'", "'See the total'"),
        ("'Siguiente pregunta'", "'Next question'"),
        ("'Siguiente tarjeta'", "'Next card'"),
        ("'Limpio.', 'Eso es.', 'Sin dudar.'", "'Clean.', 'That’s it.', 'No hesitation.'"),
        ("'Ahora ya lo sabes. Vuelve mañana en Recuerda.', 'Casi. Mira la corrección.'",
         "'Now you know. It comes back tomorrow in Recall.', 'Almost. Read the correction.'"),
        (">Respondida<", ">Answered<"),
        ("'Respondida'", "'Answered'"),
        ("'Corregida'", "'Graded'"),
        ("'Siguiente kata'", "'Next kata'"),
        ("'Responde primero ' + (needed === 3 ? 'las tres' : 'las preguntas')",
         "'Answer ' + (needed === 3 ? 'all three' : 'the questions') + ' first'"),
        ("'Ya lo hice'", "'I did it'"),
        ("'Enviado al sensei'", "'Sent to the sensei'"),
        ("'Bien. Ahora, Demuestra.'", "'Good. Now prove it.'"),
        ("'Por hoy, basta.'", "'That’s enough for today.'"),
        ("'Volver a la sala'", "'Back to the dojo'"),
        ("'Sesión cerrada'", "'Session closed'"),
        ("'Sigue.', 'Respira. Lee el slide otra vez.', 'Un paso a la vez.', 'Te sigo.'",
         "'Keep going.', 'Breathe. Read the slide again.', 'One step at a time.', 'I’m with you.'"),
        ("'Pista ' + (k + 1) + ' de ' + hints.length", "'Hint ' + (k + 1) + ' of ' + hints.length"),
        ("'Pedir ayuda al sensei'", "'Ask the sensei for help'"),
        ("'Enviado · espera aquí'", "'Sent · wait here'"),
        ("'Ya no hay más pistas aquí.'", "'No more hints here.'"),
        ("'¿Atascado? Tócame.'", "'Stuck? Touch me.'"),
    ],
    "index.html": COMMON + [
        ('title="Tócame"', 'title="Touch me"'),
        (">Continuar<", ">Continue<"),
        ("'Continuar'", "'Continue'"),
        ('title="El curriculum y por qué ves lo que ves (M)">Ver el mapa<', 'title="The curriculum, and why you see what you see (M)">See the map<'),
        ("<h2>Katas</h2>", "<h2>Katas</h2>"),
        ("Escribe <code>/dojo</code> para continuar · <code>/dojo estado</code> para ver tu progreso",
         "Type <code>/dojo</code> to continue · <code>/dojo estado</code> to see your progress"),
        ("'Te sigo.'", "'I’m with you.'"),
    ],
    "mapa.html": [
        ("<title>Dojo · Mapa</title>", "<title>Dojo · Map</title>"),
        ('title="Volver a la sala (Esc)"', 'title="Back to the dojo (Esc)"'),
        ('title="Tócame"', 'title="Touch me"'),
        ("<h1>El mapa</h1>", "<h1>The map</h1>"),
        ("{{DOMINIO}}: tu árbol de habilidades. Crece desde la raíz, abajo; cada gema es un concepto y se desbloquea al dominar las que la sostienen.",
         "{{DOMINIO}}: your skill tree. It grows from the root at the bottom; each gem is a concept and unlocks once you master the ones holding it up."),
        ("</svg>bloqueado<", "</svg>locked<"),
        ("</svg>disponible<", "</svg>available<"),
        ("</svg>visto<", "</svg>seen<"),
        ("</svg>dominado<", "</svg>mastered<"),
        ("</svg>estás aquí<", "</svg>you are here<"),
        ("</svg>camino a tu meta<", "</svg>path to your goal<"),
        ("</svg>meta<", "</svg>goal<"),
        ("</b>laguna<", "</b>gap<"),
        ("</b>duda por profundizar<", "</b>question to dig into<"),
        ("<h3>Por qué estás aquí</h3>", "<h3>Why you are here</h3>"),
        ("<h3>Lo que te falta para tu meta</h3>", "<h3>What’s left for your goal</h3>"),
        ("<h3>Lo que el dojo te debe</h3>", "<h3>What the dojo owes you</h3>"),
        (">Volver a la sala</a>", ">Back to the dojo</a>"),
        ("row('estado', d.estado) + row('puntaje', d.puntaje) + row('repaso', d.repaso) + row('depende de', d.prereq) +",
         "row('status', d.estado) + row('score', d.puntaje) + row('review', d.repaso) + row('depends on', d.prereq) +"),
        ("row('lagunas', d.lagunas) + row('dudas', d.dudas) + (d.meta === 'sí' ? row('meta', 'sí, es un ancla de tu meta') : row('camino', d.camino === 'sí' ? 'sí, te lleva a tu meta' : ''))",
         "row('gaps', d.lagunas) + row('questions', d.dudas) + (d.meta === 'sí' ? row('goal', 'yes, an anchor of your goal') : row('path', d.camino === 'sí' ? 'yes, it leads to your goal' : ''))"),
        ("row('kata', 'clic para abrirla')", "row('kata', 'click to open it')"),
    ],
}


def lang_of(dojo):
    """Idioma del aprendiz según .dojo/DOJO.md («- Idioma: en»); español si no lo dice."""
    p = Path(dojo) / "DOJO.md"
    m = re.search(r"^- Idioma:\s*([a-zA-Z]{2})", p.read_text(encoding="utf-8"), re.M) if p.exists() else None
    return m.group(1).lower() if m else "es"


def localize(shell, name, lang):
    """La plantilla `name` de assets/ en `lang`. Falla si la plantilla perdió alguna frase de la tabla."""
    if lang != "en":
        return shell
    for es, en in EN[name]:
        assert es in shell, f"{name}: falta «{es}» (actualiza scripts/idioma.py)"
        shell = shell.replace(es, en)
    return shell.replace('<html lang="es">', '<html lang="en">', 1)


def selfcheck():
    for name in EN:
        src = (ASSETS / name).read_text(encoding="utf-8")
        out = localize(src, name, "en")
        assert '<html lang="en">' in out and out.count("<script") == src.count("<script"), name
    assert localize("x", "plantilla.html", "es") == "x"
    print("selfcheck ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selfcheck"]:
        selfcheck()
    else:
        raise SystemExit(__doc__)
