"""GIFs del Sensei a partir de su dibujo real: la paleta P y draw() de assets/plantilla.html.

Uso: python docs/sensei_gif.py      (necesita playwright con Chromium y Pillow)

Ejecuta el draw() de la plantilla, sin tocarlo, en Chromium headless, frame a frame cada
100 ms, y escala cada píxel ×8 sin suavizado. Escribe docs/sensei.gif.
"""
import re
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "skills/dojo/assets/plantilla.html").read_text(encoding="utf-8")
BG = (10, 10, 11)  # --bg de la plantilla
STEP = 100  # ms por frame

palette = re.search(r"^\s*var P = \{.*?\};$", SRC, re.M).group(0)
draw = re.search(r"^  function draw\(cv, t\) \{.*?^  \}$", SRC, re.M | re.S).group(0)
PAGE = f"""<canvas id="c" width="24" height="24"></canvas><script>
var rm = false, lookUntil = 0, att = {{ gx: 0, gy: 0, blink: -1 }};
{palette}
{draw}
var cv = document.getElementById('c'); cv.__seed = 0; cv.__bowUntil = 0;
window.frame = function (o) {{
  cv.dataset.mood = o.mood; cv.dataset.look = o.look || '';
  att.gx = o.gx || 0; att.gy = o.gy || 0; att.blink = o.blink === undefined ? -1 : o.blink;
  cv.__bowUntil = o.bow ? o.t + 1 : 0;
  draw(cv, o.t);
  return Array.from(cv.getContext('2d').getImageData(0, 0, 24, 24).data);
}};
</script>"""

# (pose, duración en ms, extras). Las miradas y el parpadeo usan la misma atención que la página.
SHOW = [
    ("normal", 1200, {}), ("normal", 700, {"gx": 1}), ("normal", 700, {"gx": -1}),
    ("normal", 600, {"blink": "now"}), ("happy", 1400, {}),
    ("write", 3200, {}),
    ("bow", 1200, {"mood": "normal", "bow": True}),
    ("point", 1100, {"look": "right"}), ("point", 1100, {"look": "down"}),
    ("normal", 800, {}),
]


def frames(page, seq):
    out, t = [], 0
    for name, ms, extra in seq:
        start = t
        for _ in range(ms // STEP):
            o = {"mood": name, "t": t, **extra}
            if o.get("blink") == "now":
                o["blink"] = start
            rgba = bytes(page.evaluate("o => frame(o)", o))
            img = Image.frombytes("RGBA", (24, 24), rgba)
            out.append(Image.alpha_composite(Image.new("RGBA", (24, 24), BG + (255,)), img).convert("RGB"))
            t += STEP
    return out


def save(imgs, path, scale, pad):
    side = (24 + 2 * pad) * scale
    big = []
    for im in imgs:
        canvas = Image.new("RGB", (24 + 2 * pad, 24 + 2 * pad), BG)
        canvas.paste(im, (pad, pad))
        big.append(canvas.resize((side, side), Image.NEAREST))
    big[0].save(path, save_all=True, append_images=big[1:], duration=STEP, loop=0, optimize=True, disposal=1)
    print(f"{path.relative_to(ROOT)}  {len(big)} frames  {side}px")


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(PAGE)
    save(frames(page, SHOW), ROOT / "docs/sensei.gif", 8, 4)
    browser.close()
