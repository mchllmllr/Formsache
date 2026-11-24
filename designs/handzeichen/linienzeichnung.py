"""Handzeichen als Strichzeichnung (Stil wie Vorlage: schwarze Linie auf Holzbasis).

Jede Zeichnung besteht aus Mittellinien (SVG-Pfade). Die schwarze Lage ist die Linie mit
STROKE mm Breite und runden Enden; die Holzbasis ist dieselbe Linie mit STROKE + 2*RAND
plus die gefüllte Silhouette.

Aufruf: python3 linienzeichnung.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
STROKE = 7.0   # mm, schwarze Linie
RAND = 7.0     # mm, Holzrand um die Linie
WOOD = "#D9B382"
INK = "#1E1B19"


def u_finger(x0, x1, top, bottom):
    """Finger als U-Bogen: linke Kante hoch, runde Kuppe, rechte Kante runter."""
    r = (x1 - x0) / 2
    return f"M{x0},{bottom} L{x0},{top} A{r},{r} 0 0 1 {x1},{top} L{x1},{bottom}"


HIGH_FIVE = {
    "size": (124, 150),
    # Silhouette (für die Füllung der Basis)
    "fill": [
        u_finger(28, 48, 34, 70), u_finger(48, 68, 22, 70), u_finger(68, 88, 30, 70), u_finger(88, 105, 48, 74),
        "M28,66 L28,86 Q18,88 12,95 A8,8 0 0 0 22,109 L32,113 Q36,136 60,136 L82,136 Q105,136 105,112 L105,70 Z",
    ],
    "lines": [
        # Finger als U-Bögen; benachbarte Finger teilen sich die Kante -> Trennlinie endet frei
        "M28,86 L28,34 A10,10 0 0 1 48,34 L48,72",           # Zeigefinger (außen lang, innen kurz)
        u_finger(48, 68, 22, 72), u_finger(68, 88, 30, 72),
        "M88,72 L88,48 A8.5,8.5 0 0 1 105,48 L105,112",       # kleiner Finger (außen lang)
        # Daumen (runde Kuppe) + Boden
        "M28,86 Q18,88 12,95 A8,8 0 0 0 22,109 L32,113 Q36,136 60,136 L82,136 Q105,136 105,112",
        # Daumenfalte, läuft frei aus
        "M32,113 Q44,108 45,96",
    ],
}

PEACE = {
    "size": (112, 150),
    "fill": [
        f'<g transform="rotate(-8 28 74)"><path d="{u_finger(18, 38, 26, 74)}"/></g>',
        f'<g transform="rotate(8 64 74)"><path d="{u_finger(54, 74, 26, 74)}"/></g>',
        "M18,72 L18,112 Q18,136 44,136 L62,136 Q86,136 86,112 L86,70 L18,70 Z",
    ],
    "lines": [
        # Zeige- und Mittelfinger, leicht gespreizt
        f'<g transform="rotate(-8 28 74)"><path d="{u_finger(18, 38, 26, 74)}"/></g>',
        f'<g transform="rotate(8 64 74)"><path d="{u_finger(54, 74, 26, 74)}"/></g>',
        # linke Handkante (schließt an den Zeigefinger an) + Boden + rechte Seite
        "M18.1,75.4 L18,112 Q18,136 44,136 L62,136 Q84,136 84,118 Q84,108 76,106",
        # eingeklappter Ringfinger als Schlaufe
        "M58,76 L74,76 A8,8 0 0 1 74,92 L52,92 A8,8 0 0 1 52,76 L58,76",
        # eingeklappter kleiner Finger darunter, läuft frei nach links aus
        "M74,92 A7,7 0 0 1 76,106 L62,106",
        # Daumen: von der linken Kante schräg hoch, endet rund
        "M18,114 Q33,111 46,102",
    ],
}


def render(d, mode):
    w, h = d["size"]
    parts = []
    for p in d["lines"]:
        parts.append(p if p.startswith("<g") else f'<path d="{p}"/>')
    lines = "".join(parts)
    fill = "".join(p if p.startswith("<g") else f'<path d="{p}"/>' for p in d["fill"])
    base = (f'<g fill="{WOOD}">{fill}</g>'
            f'<g fill="none" stroke="{WOOD}" stroke-width="{STROKE + 2 * RAND}" stroke-linecap="round" '
            f'stroke-linejoin="round">{lines}</g>')
    ink = (f'<g fill="none" stroke="{INK}" stroke-width="{STROKE}" stroke-linecap="round" '
           f'stroke-linejoin="round">{lines}</g>')
    body = base + ink if mode == "vorschau" else (base if mode == "basis" else ink)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 {w + 24} {h + 24}" '
            f'width="{w + 24}mm" height="{h + 24}mm">{body}</svg>')


for name, d in {"high-five": HIGH_FIVE, "peace": PEACE}.items():
    for mode in ("vorschau", "linie", "basis"):
        with open(f"{OUT}/{name}_{mode}.svg", "w") as f:
            f.write(render(d, mode))
print("ok")
