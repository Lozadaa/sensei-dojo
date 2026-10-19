"""Reinyecta las lecciones existentes en las plantillas actuales del skill.

Uso: python scripts/refresh.py <carpeta .dojo/lessons> [--saludo "…"]

Para cada NNN-*.html conserva <title>, el cinturón (.meta) y el <main id="deck">,
y los pone en una copia fresca de assets/plantilla.html. Añade el Sensei grande a
las portadas (section.cover) que no lo tengan. Regenera index.html desde
assets/index.html conservando dominio, cinturón, filas de katas y saludo
(--saludo lo sustituye; ver references/leccion.md § Sensei). Al final regenera
lessons/mapa.html con scripts/mapa.py (leccion.md § El mapa). Marca data-done="1" en las
filas cuyo data-id está practicado o dominado en ../PROGRESS.md.
"""
import html
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
BIG = '\n  <canvas class="sensei big" width="24" height="24"></canvas>'


def grab(pattern, text, what, name):
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit(f"{name}: no encuentro {what}; no toco el archivo")
    return m.group(1)


def add_sensei(deck):
    def fix(m):
        return m.group(1) + ("" if "sensei" in m.group(2) else BIG) + m.group(2) + m.group(3)
    return re.sub(r'(<section\b[^>]*class="[^"]*\bcover\b[^"]*"[^>]*>)(.*?)(</section>)', fix, deck, flags=re.S)


def lesson(path, shell):
    old = path.read_text(encoding="utf-8")
    title = grab(r"<title>(.*?)</title>", old, "<title>", path.name)
    belt = grab(r'<div class="meta">(.*?)</div>', old, ".meta", path.name)
    raw = grab(r'<main id="deck">(.*?)</main>', old, '<main id="deck">', path.name)
    deck = add_sensei(raw)
    new = (shell.replace("<title>{{KATA}} · {{TITULO}}</title>", f"<title>{title}</title>")
                .replace("{{CINTURON}}", belt)
                .replace("\n<!-- SLIDES -->\n", deck))
    # el contenido didáctico no se pierde: mismas secciones y mismo texto fuera del Sensei
    assert not any(k in new for k in ("{{KATA}}", "{{CINTURON}}", "<!-- SLIDES -->")), path.name
    assert new.count("<section") == old.count("<section"), path.name
    assert deck.replace(BIG, "") == raw.replace(BIG, ""), path.name
    path.write_text(new, encoding="utf-8")
    print(f"ok  {path.name}  ({deck.count('<section')} slides)")


def mark_done(row, lessons):
    """data-done="1" si el concepto de la fila (data-id) está practicado o dominado en PROGRESS.md."""
    row = re.sub(r' data-done="1"', "", row)
    m, prog = re.search(r'data-id="([^"]+)"', row), lessons.parent / "PROGRESS.md"
    if m and prog.exists():
        st = re.search(r"^\|\s*" + re.escape(m.group(1)) + r"\s*\|[^|]*\|\s*([^|]*?)\s*\|", prog.read_text(encoding="utf-8"), re.M)
        if st and st.group(1).startswith(("practicado", "dominado")):
            row = row.replace('<a class="row"', '<a class="row" data-done="1"', 1)
    return row


def index(path, shell, saludo=None):
    old = path.read_text(encoding="utf-8")
    domain = grab(r"<h1>(.*?)</h1>", old, "<h1>", path.name)
    belt = grab(r'<div class="belt">(.*?)</div>', old, ".belt", path.name)
    rows = [mark_done(r, path.parent) for r in re.findall(r'<a class="row".*?</a>', old, re.S)] \
        or re.findall(r'<div class="empty">.*?</div>', old, re.S)
    if saludo is None:  # sin --saludo se conserva el que ya tenía (ya es HTML)
        m = re.search(r'<p class="greet">(.*?)</p>', old, re.S)
        greet = m.group(1) if m else ""
    else:
        greet = html.escape(saludo, quote=False)
    new = (shell.replace("{{DOMINIO}}", domain).replace("{{CINTURON}}", belt).replace("{{SALUDO}}", greet)
                .replace("<!-- KATAS -->", "<!-- KATAS -->\n" + "\n".join(rows)))
    assert all(r in new for r in rows), path.name
    path.write_text(new, encoding="utf-8")
    print(f"ok  {path.name}  ({len(rows)} katas)")


def main():
    args = sys.argv[1:]
    saludo = None
    if "--saludo" in args:
        k = args.index("--saludo")
        saludo = args[k + 1] if k + 1 < len(args) else ""
        del args[k:k + 2]
    if len(args) != 1 or not Path(args[0]).is_dir():
        raise SystemExit(__doc__)
    folder = Path(args[0])
    shell = (ASSETS / "plantilla.html").read_text(encoding="utf-8")
    for p in sorted(folder.glob("[0-9][0-9][0-9]-*.html")):
        lesson(p, shell)
    if (folder / "index.html").exists():
        index(folder / "index.html", (ASSETS / "index.html").read_text(encoding="utf-8"), saludo)
    import mapa  # siempre al final: el mapa y la frase del porqué en la sala salen del estado guardado
    mapa.build(folder)


if __name__ == "__main__":
    main()
