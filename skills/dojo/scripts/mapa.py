"""El mapa: el curriculum como árbol de prerrequisitos, pintado con el estado del aprendiz.

Uso: python scripts/mapa.py <carpeta .dojo/lessons>     (refresh.py lo llama siempre al final)
     python scripts/mapa.py --selfcheck

Lee el curriculum (.dojo/curriculum.md), PROGRESS.md,
REFUERZO.md, DUDAS.md, DOJO.md (meta y «Meta → conceptos») y las filas de lessons/index.html.
Calcula el concepto actual, el camino hasta la meta y tres frases de «por qué estás aquí»;
escribe lessons/mapa.html desde assets/mapa.html y pone la primera frase en la sala
(<p class="porque"><!-- PORQUE -->…</p> de lessons/index.html).
"""
import html
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
ID = r"[A-Z]+-[A-Z0-9]+"
DONE = ("dominado",)
STARTED = ("visto", "practicado")


# ---------- lectura ----------
def curriculum(text):
    """[(cinturón, título)], {id: {id, t, belt, prereq[], n}} en el orden del archivo."""
    belts, cs = [], {}
    for line in text.splitlines():
        m = re.match(r"^## Cinturón (\S+) · (.+?)\s*$", line)
        if m:
            belts.append((m.group(1), m.group(2)))
            continue
        m = re.match(r"^### (" + ID + r") (.+?)\s+prereq:\s*(.+?)\s*$", line)
        if m and belts:
            cs[m.group(1)] = {"id": m.group(1), "t": m.group(2).strip(), "belt": belts[-1][0],
                              "prereq": re.findall(ID, m.group(3)), "n": len(cs)}
    return belts, cs


def table(text):
    """Filas de la primera tabla markdown como dicts por cabecera."""
    rows, head = [], None
    for line in text.splitlines():
        if not line.startswith("|"):
            if head and rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            head = [h.lower() for h in cells]
        elif not set("".join(cells)) <= set("-: "):
            rows.append(dict(zip(head, cells)))
    return rows


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


def load(lessons):
    dojo = lessons.parent
    meta = read(dojo / "DOJO.md")
    cur = dojo / "curriculum.md"
    belts, cs = curriculum(read(cur))
    prog = {r.get("id"): r for r in table(read(dojo / "PROGRESS.md"))}
    katas = {}
    for row in re.findall(r'<a class="row"[^>]*>', read(lessons / "index.html")):
        i, h = re.search(r'data-id="([^"]+)"', row), re.search(r'href="([^"]+)"', row)
        if i and h:
            katas[i.group(1)] = h.group(1)
    lagunas = [r for r in table(read(dojo / "REFUERZO.md")) if r.get("estado", "").startswith("abierta")]
    dudas = [r for r in table(read(dojo / "DUDAS.md"))
             if re.match(r"(profundizar|gancho|adelantada)", r.get("acción", "")) and "resuelta" not in r.get("acción", "")]
    goal = re.search(r'^- Meta a 3 meses:\s*"?(.+?)"?\s*$', meta, re.M)
    anchors = re.search(r"^- Meta → conceptos:\s*([^(\n]+)", meta, re.M)
    title = re.search(r"^# DOJO · (.+)$", meta, re.M)
    belt = re.search(r"Cinturón:\s*(\S+)", read(dojo / "PROGRESS.md"))
    return {"belts": belts, "cs": cs, "katas": katas, "lagunas": lagunas, "dudas": dudas,
            "state": {k: v.get("estado", "nuevo").split(" (")[0] for k, v in prog.items()}, "prog": prog,
            "goal": goal.group(1) if goal else "", "anchors": re.findall(ID, anchors.group(1)) if anchors else [],
            "domain": title.group(1).strip() if title else "", "belt": belt.group(1) if belt else ""}


# ---------- cálculo ----------
def concept_of(d, raw):
    m = re.match(ID, raw or "")
    return m.group(0) if m else None


def actual(d):
    """La kata más reciente con su concepto empezado y no dominado; si no hay, el siguiente a avanzar."""
    st, cs = d["state"], d["cs"]
    for cid, href in sorted(d["katas"].items(), key=lambda kv: kv[1], reverse=True):
        if st.get(cid) in STARTED:
            return cid
    for cid, c in sorted(cs.items(), key=lambda kv: kv[1]["n"]):
        if st.get(cid) not in DONE and all(st.get(p) in DONE for p in c["prereq"]):
            return cid
    return None


def path(d):
    """Cierre de prerrequisitos de las anclas, sin lo dominado, en orden topológico (empate: orden del curriculum)."""
    cs, st, need, todo = d["cs"], d["state"], set(), [a for a in d["anchors"] if a in d["cs"]]
    while todo:
        c = todo.pop()
        if c in need or st.get(c) in DONE:
            continue
        need.add(c)
        todo += [p for p in cs[c]["prereq"] if p in cs]
    out, left = [], set(need)
    while left:
        ready = [c for c in left if not any(p in left for p in cs[c]["prereq"])]
        nxt = min(ready or left, key=lambda c: cs[c]["n"])
        out.append(nxt)
        left.discard(nxt)
    return out


def names(ids, cs):
    xs = [f"{i} {cs[i]['t']}" if i in cs else i for i in ids]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


def why(d, cur, way):
    cs, st = d["cs"], d["state"]
    if not cur:
        one = "Has dominado todo el curriculum."
    else:
        c, pre = cs[cur], cs[cur]["prereq"]
        if not pre:
            one = f"Estás en {cur} {c['t']} porque es el punto de partida del curriculum."
        else:
            ok = [p for p in pre if st.get(p) in DONE]
            one = (f"Estás en {cur} {c['t']} porque " +
                   (f"solo depende de {names(pre, cs)}, que ya dominas." if len(pre) == 1 and ok else
                    f"depende de {names(pre, cs)}, que ya dominas." if len(ok) == len(pre) else
                    f"depende de {names(pre, cs)}; aún falta dominar {names([p for p in pre if p not in ok], cs)}."))
    goal = re.split(r"[,.;]", d["goal"])[0].strip()
    if not d["anchors"]:
        two = "Aún no hay meta fijada: falta la línea «Meta → conceptos» en DOJO.md."
    elif not way:
        two = "Ya dominas todo lo que pide tu meta."
    else:
        two = f"Te faltan {len(way)} katas para tu meta" + (f" ({goal.lower()})" if goal else "") + f": la siguiente es {way[0]} {cs[way[0]]['t']}"
        belt = cs[cur]["belt"] if cur else None
        out = next((w for w in way if cs[w]["belt"] != belt), None)
        two += (f"; la primera fuera del {belt} es {out} {cs[out]['t']}." if out and belt and out != way[0] else ".")
    L, D = [r["id"] for r in d["lagunas"]], d["dudas"]
    if not L and not D:
        three = "No hay lagunas ni dudas pendientes."
    else:
        parts = []
        if L:
            parts.append(f"{len(L)} laguna{'s' if len(L) > 1 else ''} ({', '.join(L)})")
        if D:
            parts.append(f"profundizar {len(D)} duda{'s' if len(D) > 1 else ''} ({', '.join(r['id'] for r in D)})")
        three = "El dojo te debe " + " y ".join(parts) + "."
    return [one, two, three]


# ---------- dibujo: árbol de habilidades ----------
# Crece hacia arriba desde la raíz: cada concepto en la fila de su profundidad (el camino más
# largo de prerrequisitos) y, en horizontal, bajo la media de sus padres; los hermanos se
# reparten a ambos lados. Gemas pixel de 32 px con un glifo por estado; conectores en codo
# que giran en el hueco entre filas, nunca sobre una etiqueta.
WIDTH, ROW, R, SPREAD, PAD = 1272, 72, 16, 196, 24
GLYPH = {  # 7×7, a escala 2 en el centro de la gema
    "dominado": "M0 3h1v1H0zM1 4h1v1H1zM2 5h1v1H2zM3 4h1v1H3zM4 3h1v1H4zM5 2h1v1H5zM6 1h1v1H6z",
    "practicado": "M1 1h5v5H1z",
    "visto": "M2 2h3v1H2zM2 4h3v1H2zM2 3h1v1H2zM4 3h1v1H4z",
    "cur": "M2 2h3v3H2z",
    "open": "M3 1h1v5H3zM1 3h5v1H1z",
    "lock": "M2 0h3v1H2zM1 1h1v2H1zM5 1h1v2H5zM0 3h7v4H0z",
}


def gem(cx, cy, r=R, c=6):
    """Octógono pixel: esquinas en escalera de 2 px (sentido horario desde arriba a la izquierda)."""
    steps = c // 2
    q = []  # cuarto de arriba a la derecha: de la cara superior a la derecha, en escalones
    for k in range(steps):
        q += [(r - c + 2 * k, -r + 2 * k), (r - c + 2 * k + 2, -r + 2 * k)]
    q.append((r, -r + c))
    pts = [(-(r - c), -r)] + q
    pts += [(x, -y) for x, y in reversed(q)]                  # abajo a la derecha
    pts += [(-x, -y) for x, y in q]                           # abajo a la izquierda
    pts += [(-x, y) for x, y in reversed(q)]                  # arriba a la izquierda
    return "M" + " L".join(f"{cx + x} {cy + y}" for x, y in pts) + " Z"


def depths(cs):
    memo = {}

    def dep(c):
        if c not in memo:
            memo[c] = 1 + max((dep(p) for p in cs[c]["prereq"] if p in cs), default=-1)
        return memo[c]
    return {c: dep(c) for c in cs}


def layout(cs):
    dep = depths(cs)
    top = max(dep.values(), default=0)
    xs = {}
    for r in range(top + 1):
        row = [c for c in cs if dep[c] == r]
        want = {}
        for c in row:
            ps = [xs[p] for p in cs[c]["prereq"] if p in xs]
            want[c] = sum(ps) / len(ps) if ps else WIDTH / 2
        row.sort(key=lambda c: (want[c], cs[c]["n"]))
        got = []
        for c in row:
            got.append(max(want[c], got[-1] + SPREAD) if got else want[c])
        shift = sum(want[c] for c in row) / len(row) - sum(got) / len(got)  # la fila, centrada bajo sus padres
        lo, hi = R + 8, WIDTH - SPREAD + 16
        shift = max(lo - got[0], min(shift, hi - got[-1]))
        for c, x in zip(row, got):
            xs[c] = round(x + shift)
    lo, hi = min(xs.values()) - R, max(xs.values()) + SPREAD - 16  # el árbol entero, centrado en el lienzo
    dx = round((WIDTH - (hi - lo)) / 2 - lo)
    pos = {c: (xs[c] + dx, PAD + 24 + (top - dep[c]) * ROW + R) for c in cs}
    return pos, (top + 1) * ROW + PAD + 24


def wrap(t, n=22):
    words, lines = t.split(), [""]
    for w in words:
        if len(lines[-1]) + len(w) + (1 if lines[-1] else 0) > n and lines[-1]:
            lines.append(w)
        else:
            lines[-1] = (lines[-1] + " " + w).strip()
    return lines[:2] if len(lines) <= 2 else [lines[0], " ".join(lines[1:])[:n - 1] + "…"]


def svg(d, cur, way):
    cs, st = d["cs"], d["state"]
    pos, height = layout(cs) if cs else ({}, 80)
    onway, lag, dud = set(way), {}, {}
    for r in d["lagunas"]:
        lag.setdefault(concept_of(d, r.get("concepto")), []).append(r["id"])
    for r in d["dudas"]:
        dud.setdefault(concept_of(d, r.get("concepto")), []).append(r)
    out = [f'<svg class="dg tree" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" role="img" aria-label="Árbol de habilidades del curriculum">',
           '<defs><pattern id="grid8" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" class="dot"/></pattern>'
           '<pattern id="pdots" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#e9e4d8" fill-opacity=".5"/></pattern></defs>',
           f'<rect class="bg" width="{WIDTH}" height="{height}" fill="url(#grid8)"/>']
    # conectores: suben del padre, giran en el hueco justo encima de él y entran al hijo por debajo
    for c in cs.values():
        cx, cy = pos[c["id"]]
        for p in c["prereq"]:
            if p not in pos:
                continue
            px, py = pos[p]
            mid = py - R - 10  # el codo, en el hueco sobre la gema padre: bajo las etiquetas de la fila de arriba
            cls = ("ln done" if st.get(p) in DONE and st.get(c["id"]) in DONE else
                   "ln hot" if c["id"] in onway else "ln")
            out.append(f'<path class="{cls}" d="M{px}.5 {py - R} V{mid}.5 H{cx}.5 V{cy + R}"/>')
    for cid, c in cs.items():
        cx, cy = pos[cid]
        s = st.get(cid, "nuevo")
        s = s if s in ("visto", "practicado", "dominado") else "nuevo"
        ready = all(st.get(p) in DONE for p in c["prereq"])
        cls = ["node", s] + ([] if s != "nuevo" else ["open" if ready else "lock"])
        cls += (["way"] if cid in onway else []) + (["cur"] if cid == cur else []) + (["goal"] if cid in d["anchors"] else [])
        p = d["prog"].get(cid, {})
        data = {"id": cid, "t": c["t"], "belt": c["belt"], "estado": s + ("" if s != "nuevo" else " · disponible" if ready else " · bloqueado"),
                "puntaje": p.get("puntaje", "—"), "repaso": p.get("repaso", "—"), "prereq": ", ".join(c["prereq"]) or "—",
                "lagunas": " · ".join(f"{r['id']} {r.get('lo que no supo', '')}" for r in d["lagunas"] if concept_of(d, r.get("concepto")) == cid),
                "dudas": " · ".join(f"{r['id']} {r.get('acción', '')}" for r in dud.get(cid, [])),
                "camino": "sí" if cid in onway else "no", "meta": "sí" if cid in d["anchors"] else "no"}
        attrs = " ".join(f'data-{k}="{html.escape(v, quote=True)}"' for k, v in data.items())
        href = d["katas"].get(cid)
        g = [f'<a class="{" ".join(cls)}" href="{href}" {attrs}>' if href else f'<a class="{" ".join(cls)}" tabindex="0" {attrs}>']
        if cid in d["anchors"]:
            g.append(f'<path class="ring" d="{gem(cx, cy, R + 5, 8)}"/>')
        g.append(f'<path class="gem" d="{gem(cx, cy)}"/>')
        glyph = GLYPH["cur" if cid == cur else s if s != "nuevo" else "open" if ready else "lock"]
        g.append(f'<path class="glyph" transform="translate({cx - 7} {cy - 7}) scale(2)" d="{glyph}"/>')
        tags = "".join(f'<tspan class="lagt"> · {l}</tspan>' for l in lag.get(cid, []))
        tags += '<tspan class="lagt"> · ?</tspan>' if any(r.get("acción", "").startswith("profundizar") for r in dud.get(cid, [])) else ""
        tags += '<tspan class="tag"> · META</tspan>' if cid in d["anchors"] else ""
        g.append(f'<text class="cid" x="{cx + R + 12}" y="{cy - 4}">{cid}{tags}</text>')
        for k, line in enumerate(wrap(c["t"])):
            g.append(f'<text class="ct" x="{cx + R + 12}" y="{cy + 13 + 17 * k}">{html.escape(line)}</text>')
        g.append("</a>")
        out.append("".join(g))
    out.append("</svg>")
    return "\n".join(out), (pos[cur] if cur in pos else None), WIDTH


def falta(d, way):
    cs = d["cs"]
    if not way:
        return '<p class="dim">Nada: tu meta está cubierta.</p>'
    items = "".join(f'<li><code>{w}</code> {html.escape(cs[w]["t"])} <span>{cs[w]["belt"]}</span></li>' for w in way)
    mins = len(way) * 15
    return f'<ol class="falta">{items}</ol><p class="sum">{len(way)} katas, unas {mins // 60} h {mins % 60:02d} min.</p>'


def debe(d):
    cs, out = d["cs"], []
    for r in d["lagunas"]:
        c = concept_of(d, r.get("concepto"))
        out.append(f'<li><b>{r["id"]}</b> {html.escape(cs[c]["t"] if c in cs else r.get("concepto", ""))}: '
                   f'{html.escape(r.get("lo que no supo", ""))} <span>próxima {html.escape(r.get("próxima", "—"))}</span></li>')
    for r in d["dudas"]:
        c = concept_of(d, r.get("concepto"))
        out.append(f'<li><b>{r["id"]}</b> {html.escape(cs[c]["t"] if c in cs else r.get("concepto", ""))}: '
                   f'{html.escape(r.get("acción", ""))}</li>')
    return f'<ul class="debe">{"".join(out)}</ul>' if out else '<p class="dim">Nada pendiente.</p>'


def sensei_js():
    """El Sensei de la sala (una sola fuente): su IIFE de assets/index.html."""
    s = (ASSETS / "index.html").read_text(encoding="utf-8")
    a, b = s.index("/* Sensei:"), s.index("/* Sala:")
    return s[a:b].rstrip()


def build(lessons):
    d = load(lessons)
    cur = actual(d)
    way = path(d)
    lines = why(d, cur, way)
    tree, perch, width = svg(d, cur, way)
    sensei = (f'<canvas class="sensei perchnode" width="24" height="24" data-size="24" style="left:{perch[0]}px;top:{perch[1]}px"></canvas>'
              if perch else "")
    page = (ASSETS / "mapa.html").read_text(encoding="utf-8")
    for k, v in {"{{DOMINIO}}": html.escape(d["domain"]), "{{CINTURON}}": html.escape(("Cinturón " + d["belt"]) if d["belt"] else ""),
                 '"{{PORQUE1}}"': json.dumps(lines[0], ensure_ascii=False), "{{ANCHO}}": str(width)}.items():
        page = page.replace(k, v)
    page = (page.replace("<!-- MAPA -->", tree + "\n" + sensei)
                .replace("<!-- PORQUE -->", "".join(f"<p>{html.escape(x)}</p>" for x in lines))
                .replace("<!-- FALTA -->", falta(d, way)).replace("<!-- DEBE -->", debe(d))
                .replace("/* SENSEI */", sensei_js()))
    (lessons / "mapa.html").write_text(page, encoding="utf-8")
    idx = lessons / "index.html"
    if idx.exists():
        s = idx.read_text(encoding="utf-8")
        s2 = re.sub(r'(<p class="porque"><!-- PORQUE -->).*?(</p>)', lambda m: m.group(1) + html.escape(lines[0]) + m.group(2), s, flags=re.S)
        if s2 != s:
            idx.write_text(s2, encoding="utf-8")
    print(f"ok  mapa.html  (actual {cur or '—'} · camino {len(way)} · lagunas {len(d['lagunas'])} · dudas {len(d['dudas'])})")
    return d, cur, way, lines


def selfcheck():
    cur_md = """## Cinturón blanco · Base
### T-A1 Uno            prereq: —
### T-A2 Dos            prereq: T-A1
### T-A3 Tres            prereq: T-A1
## Cinturón amarillo · Más
### T-B1 Cuatro            prereq: T-A2
### T-B2 Cinco            prereq: T-B1, T-A3
"""
    belts, cs = curriculum(cur_md)
    assert [b for b, _ in belts] == ["blanco", "amarillo"] and cs["T-B2"]["prereq"] == ["T-B1", "T-A3"] and cs["T-A1"]["prereq"] == []
    d = {"belts": belts, "cs": cs, "katas": {"T-A1": "001-a.html", "T-A2": "002-b.html", "T-A3": "003-c.html"},
         "state": {"T-A1": "dominado", "T-A2": "visto", "T-A3": "nuevo"}, "prog": {}, "anchors": ["T-B2"], "goal": "Hacer cosas, y más",
         "lagunas": [{"id": "L1", "concepto": "T-A2", "estado": "abierta"}], "dudas": [], "domain": "", "belt": ""}
    assert actual(d) == "T-A2", actual(d)          # 003 existe pero T-A3 está «nuevo»: la actual es la empezada
    assert path(d) == ["T-A2", "T-A3", "T-B1", "T-B2"], path(d)
    w = why(d, "T-A2", path(d))
    assert "solo depende de T-A1 Uno" in w[0] and "Te faltan 4 katas" in w[1] and "T-B1 Cuatro" in w[1] and "L1" in w[2], w
    d["state"] = {"T-A1": "dominado", "T-A2": "dominado", "T-A3": "dominado"}
    assert actual(d) == "T-B1" and path(d) == ["T-B1", "T-B2"]   # todo lo visto dominado: el siguiente a avanzar
    assert table("| id | x |\n|---|---|\n| L1 | a |\n") == [{"id": "L1", "x": "a"}]
    assert wrap("Ramas remotas y seguimiento") == ["Ramas remotas y", "seguimiento"]
    pos, _ = layout(cs)
    assert pos["T-A1"][1] > pos["T-A2"][1] > pos["T-B1"][1] > pos["T-B2"][1]  # crece hacia arriba
    assert abs(pos["T-A2"][0] - pos["T-A3"][0]) >= SPREAD  # hermanos a ambos lados del padre
    assert gem(0, 0).count("L") == 4 * 7  # octógono: 4 esquinas en escalera de 7 puntos
    print("selfcheck ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selfcheck"]:
        selfcheck()
    elif len(sys.argv) == 2 and Path(sys.argv[1]).is_dir():
        build(Path(sys.argv[1]))
    else:
        raise SystemExit(__doc__)
