"""Sirve las lecciones del dojo y es el canal entre la presentación y el sensei.

Uso: python scripts/serve.py [carpeta .dojo/lessons] [--port 8766]

GET   sirve archivos como `python -m http.server`, pero sin listar carpetas (404) y
      sin caché, para que una kata regenerada se vea al recargar.
POST  /signal con JSON {type, kata, slide, q, text, extra}: añade una línea con `ts` a
      <carpeta .dojo>/signals.jsonl y responde 204. El sensei la vigila con Monitor.
GET   /feedback?since=N: las líneas de <carpeta .dojo>/feedback.jsonl desde la N
      (0 = primera) como array JSON; una línea ilegible llega como null para que los
      índices no se desplacen. Las escribe el sensei (references/leccion.md § Canal web).
GET   /status: {"sensei": true|false, "age": s}. true si scripts/vigila.py (el Monitor del sensei)
      tocó <carpeta .dojo>/sensei.alive hace menos de ALIVE s; la página lo enseña.
GET   /signals?kata=K&since=N: solo lectura y solo las dudas (type message) de la kata K,
      como [{ts, slide, text}] desde la N; el panel "Tengo una duda" rehace con ellas su
      historial. Ningún otro tipo de señal sale por aquí.

Hoja de respuestas: <lessons>/NNN-slug.key.json (nunca se sirve). Si una respuesta (answer o
recall) casa con ella, serve.py escribe la grade él mismo ("by": "key") y marca la señal
"graded": "key"; si no, la señal queda para la IA. Con "next" en la key, next/continue
reciben next_ready al instante ("handled": "key"). Formato en references/leccion.md.
Comprobación: python scripts/serve.py --selfcheck
"""
import json
import re
import socket
import sys
import threading
import time
import unicodedata
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

TYPES = {"done", "help", "next", "continue", "answer", "recall", "message"}
FIELDS = ("type", "kata", "slide", "q", "text", "extra")
LOCK = threading.Lock()


KEYS = {}  # ruta de la key -> (mtime, contenido); se relee si cambia


def norm(text):
    """Sin mayúsculas ni acentos, espacios colapsados y sin puntuación final."""
    text = "".join(c for c in unicodedata.normalize("NFKD", str(text).lower()) if not unicodedata.combining(c))
    return re.sub(r"[\s.,;:!?¡¿]+$", "", re.sub(r"\s+", " ", text).strip())


def matches(rule, text):
    m = str(rule.get("match", ""))
    if m.startswith("re:"):
        return any(re.search(m[3:], t, re.I) for t in (text, norm(text)))
    return norm(m) == norm(text)


def judge(entry, text):
    """(score, text, mood) si la key decide; None si la respuesta tiene que verla la IA."""
    if not isinstance(entry, dict) or not text:
        return None
    full, partial, wrong = entry.get("full") or [], entry.get("partial") or [], entry.get("wrong") or {}
    for score, group, mood in ((2, full, "happy"), (1, partial, "focused")):
        for rule in group:
            if matches(rule, text):
                say = rule.get("text") or next((r["text"] for r in group + full if r.get("text")), "")
                return score, say, rule.get("mood") or mood
    if wrong.get("auto"):
        return 0, wrong.get("text", ""), wrong.get("mood", "surprised")
    return None


def done_say(key):
    """(text, mood) del "Ya lo hice" si la key lo trae; None si lo responde la IA."""
    done = key.get("done") if isinstance(key, dict) else None
    if isinstance(done, dict) and done.get("text"):
        return str(done["text"]), done.get("mood") or "point"
    return None


ALIVE = 12  # s sin latido para darlo por desconectado (vigila.py late cada 2 s)


def status(path, now):
    """¿Escucha el sensei? Según la edad del latido de vigila.py."""
    try:
        age = now - path.stat().st_mtime
    except OSError:
        return {"sensei": False, "age": None}
    return {"sensei": age < ALIVE, "age": round(age)}


def selfcheck():
    entry = {"full": [{"match": r"re:\badd\b[\s\S]*\bcommit\b", "text": "add y commit.", "mood": "happy"}, {"match": "add y commit"}],
             "partial": [{"match": r"re:^\s*(git\s+)?add\s*$", "text": "Falta commit."}], "wrong": {"text": "No.", "auto": True}}
    assert judge(entry, "Add y Commit.") == (2, "add y commit.", "happy")
    assert judge(entry, "primero git add, luego git commit") == (2, "add y commit.", "happy")
    assert judge(entry, " git add ") == (1, "Falta commit.", "focused")
    assert judge(entry, "ninguno") == (0, "No.", "surprised")
    assert judge({"full": [{"match": "minúscula b", "text": "b"}]}, "Minuscula   B!") == (2, "b", "happy")
    assert judge({"full": [{"match": "F"}]}, "otra cosa") is None  # sin wrong auto: a la IA
    assert norm("  Ctrl + Shift + S.  ") == "ctrl + shift + s"
    assert done_say({"done": {"text": "Bien. A Demuestra."}}) == ("Bien. A Demuestra.", "point")
    assert done_say({"done": {"text": "Hecho.", "mood": "happy"}}) == ("Hecho.", "happy")
    assert done_say({"questions": {}}) is None and done_say({"done": {}}) is None  # sin done: la IA
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        beat = Path(d) / "sensei.alive"
        assert status(beat, time.time()) == {"sensei": False, "age": None}
        beat.touch()
        assert status(beat, time.time())["sensei"] and not status(beat, time.time() + ALIVE + 1)["sensei"]
    print("selfcheck ok")


def parse(line):
    try:
        return json.loads(line)
    except ValueError:
        return None


class Dojo(SimpleHTTPRequestHandler):
    error_message_format = ('<!doctype html><meta charset="utf-8"><title>%(code)d</title>'
                            '<body style="background:#0a0a0b;color:#9a948a;font:17px Georgia,serif;padding:72px 16px">'
                            '%(code)d · %(message)s · <a href="/" style="color:#d0432f">volver a la sala</a></body>')
    dojo = None  # carpeta .dojo, la fija main()
    lessons = None  # carpeta de lecciones, la fija main()

    def send_head(self):
        # las hojas de respuestas nunca salen (tampoco con trucos de Windows: "x.key.json." o "::$DATA")
        path = unquote(urlsplit(self.path).path).lower()
        if ".key.json" in path or ":" in path:
            self.send_error(404, "No existe")
            return None
        return super().send_head()

    def key(self, kata):
        if not re.fullmatch(r"[\w.-]+", str(kata or "")):
            return None
        p = self.lessons / f"{kata}.key.json"
        try:
            mtime = p.stat().st_mtime
        except OSError:
            return None
        if KEYS.get(p, (None,))[0] != mtime:
            try:
                KEYS[p] = (mtime, json.loads(p.read_text(encoding="utf-8")))
            except ValueError:  # key ilegible: todo va a la IA
                KEYS[p] = (mtime, None)
        data = KEYS[p][1]
        return data if isinstance(data, dict) else None

    def finished(self, kata, key):
        """Todas las preguntas de Demuestra de la key tienen ya una grade en feedback.jsonl."""
        f = self.dojo / "feedback.jsonl"
        lines = [parse(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.exists() else []
        done = {f"{l.get('slide')}:{l.get('q')}" for l in lines if isinstance(l, dict) and l.get("type") == "grade" and l.get("kata") == kata}
        return bool(key.get("questions")) and set(key["questions"]) <= done

    def by_key(self, line):
        """Lo que la key resuelve sin la IA: una línea para feedback.jsonl, o None."""
        key = self.key(line.get("kata"))
        if not key:
            return None
        base = {"ts": line["ts"], "kata": line["kata"], "by": "key"}
        if line["type"] in ("answer", "recall"):
            group = key.get("questions" if line["type"] == "answer" else "recall") or {}
            got = judge(group.get(f"{line.get('slide')}:{line.get('q')}"), line.get("text"))
            if got:
                line["graded"] = "key"
                return {**base, "type": "grade", "slide": line.get("slide"), "q": line.get("q"),
                        "score": got[0], "text": got[1], "mood": got[2]}
        if line["type"] == "done":
            got = done_say(key)
            if got:
                line["handled"] = "key"
                return {**base, "type": "say", "text": got[0], "mood": got[1]}
        if line["type"] in ("next", "continue"):
            nxt = str(key.get("next") or "")
            if line["type"] == "continue" and not self.finished(line["kata"], key):
                nxt = f"{line['kata']}.html"  # la kata está a medias: Continuar la reabre
            if re.fullmatch(r"[\w.-]+\.html", nxt) and (self.lessons / nxt).is_file():
                title = re.search(r"<title>(.*?)</title>", (self.lessons / nxt).read_text(encoding="utf-8"), re.S)
                line["handled"] = "key"
                return {**base, "type": "next_ready", "url": nxt, "title": title.group(1).strip() if title else ""}
        return None

    def list_directory(self, path):
        self.send_error(404, "No existe")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/status":
            return self.json(status(self.dojo / "sensei.alive", time.time()))
        if url.path not in ("/feedback", "/signals"):
            return super().do_GET()
        query = parse_qs(url.query)
        try:
            since = max(0, int(query.get("since", ["0"])[0]))
        except ValueError:
            return self.send_error(400, "since no válido")
        f = self.dojo / (url.path[1:] + ".jsonl")
        # las líneas en blanco no cuentan, ni para el índice ni para la respuesta
        lines = [parse(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.exists() else []
        if url.path == "/signals":
            kata = query.get("kata", [""])[0]
            lines = [{"ts": l.get("ts"), "slide": l.get("slide"), "text": l.get("text")} for l in lines
                     if isinstance(l, dict) and l.get("type") == "message" and l.get("kata") == kata]
        self.json(lines[since:])

    def json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/signal":
            return self.send_error(404, "No existe")
        try:
            n = int(self.headers.get("Content-Length", 0))
            if not 0 < n <= 8192:
                raise ValueError("tamaño")
            data = json.loads(self.rfile.read(n))
            if not isinstance(data, dict) or data.get("type") not in TYPES:
                raise ValueError("type")
        except ValueError:  # JSONDecodeError también es ValueError
            return self.send_error(400, "Señal no válida")
        line = {"ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                **{k: data[k] for k in FIELDS if data.get(k) is not None}}
        with LOCK:
            reply = self.by_key(line)  # antes de anotar la señal: le añade graded/handled
            with (self.dojo / "signals.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
            if reply:
                with (self.dojo / "feedback.jsonl").open("a", encoding="utf-8") as f:
                    f.write(json.dumps(reply, ensure_ascii=False) + "\n")
        self.send_response(204)
        self.end_headers()


def main():
    args = sys.argv[1:]
    if args == ["--selfcheck"]:
        return selfcheck()
    port = 8766
    if "--port" in args:
        k = args.index("--port")
        port = int(args[k + 1])
        del args[k:k + 2]
    folder = Path(args[0] if args else ".dojo/lessons").resolve()
    if len(args) > 1 or not folder.is_dir():
        raise SystemExit(__doc__)
    Dojo.dojo, Dojo.lessons = folder.parent, folder
    (Dojo.dojo / "signals.jsonl").touch()  # existe desde el principio: el vigilante puede hacer tail -f ya
    handler = partial(Dojo, directory=str(folder))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    # "localhost" prueba ::1 primero: sin escuchar ahí, Windows tarda ~2 s en caer a 127.0.0.1
    try:
        v6 = type("V6", (ThreadingHTTPServer,), {"address_family": socket.AF_INET6})(("::1", port), handler)
        threading.Thread(target=v6.serve_forever, daemon=True).start()
    except OSError:
        pass  # sin IPv6: solo 127.0.0.1
    print(f"dojo: http://localhost:{port}/  ·  canal en {Dojo.dojo}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
