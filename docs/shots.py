"""Capturas del README a partir del dojo de demostración (demo/.dojo, Git).

Uso: python docs/shots.py      (necesita playwright con Chromium)

Sirve demo/.dojo/lessons con scripts/serve.py en el puerto 8791, recorre la sala, la
kata 05 (con una respuesta enviada de verdad y corregida por la hoja de respuestas), el
panel de dudas y el mapa, y guarda los PNG en docs/. Al acabar deja signals.jsonl y
feedback.jsonl del demo como estaban.
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PORT = 8791
BASE = f"http://localhost:{PORT}/"
KATA = BASE + "005-undo-without-fear.html"

DEMO = ROOT / "demo/.dojo"
saved = {n: (DEMO / n).read_bytes() for n in ("signals.jsonl", "feedback.jsonl")}
server = subprocess.Popen([sys.executable, str(ROOT / "skills/dojo/scripts/serve.py"),
                           str(ROOT / "demo/.dojo/lessons"), "--port", str(PORT)])
try:
    for _ in range(50):
        try:
            urllib.request.urlopen(BASE, timeout=1)
            break
        except OSError:
            time.sleep(.2)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1)
        page.add_init_script("Math.random = () => 0.5;")  # miradas del Sensei estables entre capturas

        def shot(url, name, wait=1500, full=False, before=None):
            page.goto(url)
            page.mouse.move(800, 980)
            page.wait_for_timeout(wait)
            if before:
                before()
            page.screenshot(path=str(ROOT / "docs" / f"{name}.png"), full_page=full)
            print("docs/" + name + ".png")

        shot(BASE, "sala")
        shot(KATA + "#1", "kata-portada", wait=2600)
        shot(KATA + "#7", "kata-haz")
        def answer():
            page.locator("[placeholder='Your answer']:visible").first.fill("git restore --staged notes.txt")
            page.get_by_role("button", name="Send").first.click()
            page.wait_for_timeout(1500)
            page.screenshot(path=str(ROOT / "docs/kata-corrigiendo.png"))  # el Sensei escribe la nota
            print("docs/kata-corrigiendo.png")
            page.wait_for_timeout(3000)  # la key corrige al instante; la página la enseña tras ≥ 3 s de escritura
        shot(KATA + "#8", "kata-demuestra", before=answer)

        def open_doubts():
            page.get_by_role("button", name="I have a question").first.click()
            page.wait_for_timeout(1200)
        shot(KATA + "#4", "kata-duda", before=open_doubts)
        shot(BASE + "mapa.html", "mapa", full=True)
        b.close()
finally:
    server.terminate()
    server.wait()
    for n, b in saved.items():
        (DEMO / n).write_bytes(b)

# sin los márgenes vacíos: a la anchura de un README, el texto se lee
CROP = {"sala": (296, 0, 1304, 1000), "kata-portada": (296, 0, 1304, 1000), "kata-haz": (296, 0, 1304, 1000),
        "kata-corrigiendo": (296, 0, 1304, 1000), "kata-demuestra": (296, 0, 1304, 1000), "kata-duda": (296, 0, 1600, 1000)}
for name, box in CROP.items():
    f = ROOT / "docs" / f"{name}.png"
    Image.open(f).crop(box).save(f, optimize=True)
f = ROOT / "docs/mapa.png"
im = Image.open(f)
im.crop((120, 0, 1480, im.height)).save(f, optimize=True)
