"""El vigilante del sensei: lo que el Monitor ejecuta mientras hay una kata o la sala abierta.

Uso: python scripts/vigila.py [carpeta .dojo]      (Monitor, timeout 30 min, rearmar al expirar)

Imprime cada línea nueva de <dojo>/signals.jsonl (una por evento del Monitor) y cada 2 s toca
<dojo>/sensei.alive. serve.py responde GET /status con ese latido: si el vigilante muere (el
Monitor expira o se cierra la sesión) el latido se para y la página enseña al Sensei
desconectado. Por eso sustituye a `tail -F`: el latido vive y muere con quien escucha.
"""
import sys
import time
from pathlib import Path


def main():
    dojo = Path(sys.argv[1] if len(sys.argv) > 1 else ".dojo").resolve()
    if not dojo.is_dir():
        raise SystemExit(__doc__)
    sig, alive = dojo / "signals.jsonl", dojo / "sensei.alive"
    sig.touch()
    pos = sig.stat().st_size  # solo lo que llegue desde ahora, como tail -n0
    rest = b""
    while True:
        alive.touch()
        size = sig.stat().st_size
        if size < pos:  # truncado: no debería pasar (append-only), pero no te quedes ciego
            pos = 0
        if size > pos:
            with sig.open("rb") as f:
                f.seek(pos)
                rest += f.read()
                pos = f.tell()
            *lines, rest = rest.split(b"\n")
            for line in lines:
                if line.strip():
                    print(line.decode("utf-8", "replace"), flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
