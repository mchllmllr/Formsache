"""Handzeichen als Strichzeichnung (Stil wie Vorlage: schwarze Linie auf Holzbasis).

Jede Zeichnung besteht aus Mittellinien (SVG-Pfade). Die schwarze Lage ist die Linie mit
STROKE mm Breite und runden Enden; die Holzbasis ist dieselbe Linie mit STROKE + 2*RAND
plus die gefüllte Silhouette.

Aufruf: python3 linienzeichnung.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
STROKE = 5.0   # mm, schwarze Linie (schlank, ca. 4 % der Handbreite)
RAND = 6.5     # mm, Holzrand um die Linie
WOOD = "#D9B382"
INK = "#1E1B19"


def u_finger(x0, x1, top, bottom):
    """Finger als U-Bogen: linke Kante hoch, runde Kuppe, rechte Kante runter."""
    r = (x1 - x0) / 2
    return f"M{x0},{bottom} L{x0},{top} A{r},{r} 0 0 1 {x1},{top} L{x1},{bottom}"


HIGH_FIVE = {
    "size": (100, 176),
    "fill": [
        "M26,100 L26,34 A8.5,8.5 0 0 1 43,34 L43,22 A8.5,8.5 0 0 1 60,22 L60,30 A8.5,8.5 0 0 1 77,30 "
        "L77,52 A8,8 0 0 1 93,52 L93,128 C93,156 82,170 62,170 L50,170 C34,170 30,158 28,146 "
        "C16,136 2,110 4,96 C6,84 18,88 26,104 Z",
    ],
    "lines": [
        # Finger: lang und schlank; Trennlinien enden frei am Handflächenansatz
        "M26,108 L26,34 A8.5,8.5 0 0 1 43,34 L43,92",
        "M43,40 L43,22 A8.5,8.5 0 0 1 60,22 L60,92",
        "M60,40 L60,30 A8.5,8.5 0 0 1 77,30 L77,92",
        "M77,60 L77,52 A8,8 0 0 1 93,52 L93,128",
        # rechte Seite, Boden, Daumen als fließende Kurve
        "M93,128 C93,156 82,170 62,170 L50,170 C34,170 30,158 28,146 "
        "C16,136 2,110 4,96 C6,84 18,88 26,104",
        # Daumenfalte, schwingt frei aus
        "M28,146 C38,138 41,126 37,114",
    ],
}

PEACE = {
    "size": (100, 176),
    "fill": [
        f'<g transform="rotate(-7 30 96)"><path d="M21,96 L21,22 A9,9 0 0 1 39,22 L39,96 Z"/></g>',
        f'<g transform="rotate(7 62 96)"><path d="M53,96 L53,22 A9,9 0 0 1 71,22 L71,96 Z"/></g>',
        "M21,92 L86,92 L86,140 C86,160 76,170 56,170 L46,170 C26,170 21,156 21,140 Z",
    ],
    "lines": [
        # Zeige- und Mittelfinger, lang, leicht gespreizt
        '<g transform="rotate(-7 30 96)"><path d="M21,104 L21,22 A9,9 0 0 1 39,22 L39,96"/></g>',
        '<g transform="rotate(7 62 96)"><path d="M53,96 L53,22 A9,9 0 0 1 71,22 L71,99"/></g>',
        # eingerollter Ringfinger: Schlaufe nach links
        "M71,99 L82,99 C90,99 90,115 82,115 L62,115 C53,115 53,99 62,99 L71,99",
        # eingerollter kleiner Finger darunter
        "M82,115 C90,115 89,131 80,131 L66,131",
        # Handkante links, Boden, rechte Seite bis unter den kleinen Finger
        "M22,104 L21,140 C21,156 26,170 46,170 L56,170 C76,170 86,160 86,142 C86,136 84,132 80,131",
        # Daumen: fließende Kurve von links, endet vor den eingerollten Fingern
        "M21,140 C30,138 40,132 46,122",
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
