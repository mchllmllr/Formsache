"""Erzeugt die Handzeichen-Entwürfe als SVG (Einheiten: mm).

Variante A: Holzplatte mit gedruckten Streifen (xTool) + Hand (Bambu)
Variante B: nur die Hand (Bambu)

Aufruf: python3 generate.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
# Emoji-Look: warmes Gelb, Kontur in Honigbraun statt Schwarz
OUTLINE = "#B86B12"
HAND = "#FFC93C"


def capsule(cx, base_y, length, width, angle):
    r = width / 2
    return (f'<rect x="{cx - r:.2f}" y="{base_y - length:.2f}" width="{width:.2f}" '
            f'height="{length:.2f}" rx="{r:.2f}" transform="rotate({angle} {cx:.2f} {base_y:.2f})"/>')


def high_five():
    shapes = [
        '<rect x="42" y="76" width="66" height="72" rx="28"/>',  # Handfläche, rund
        capsule(53, 98, 56, 17, -11),     # Zeigefinger
        capsule(70, 94, 62, 17.5, -2),    # Mittelfinger
        capsule(87, 96, 56, 17, 6),       # Ringfinger
        capsule(101, 106, 42, 15.5, 15),  # kleiner Finger
        capsule(52, 120, 32, 19, -55),    # Daumen
    ]
    return shapes, []


def peace():
    shapes = [
        '<rect x="44" y="84" width="62" height="66" rx="26"/>',  # Handfläche, rund
        capsule(63, 102, 62, 17.5, -17),  # Zeigefinger
        capsule(84, 102, 64, 17.5, 15),   # Mittelfinger
        '<rect x="78" y="88" width="32" height="17" rx="8.5"/>',  # Ringfinger eingeklappt
        '<rect x="80" y="104" width="29" height="16" rx="8"/>',   # kleiner Finger eingeklappt
        '<rect x="38" y="110" width="50" height="18" rx="9" transform="rotate(-12 63 119)"/>',  # Daumen
    ]
    # Nur die Trennlinien der eingeklappten Finger – ohne sie liest man das Peace-Zeichen nicht.
    lines = ['<path d="M83,105 h23"/>', '<path d="M85,120 h21"/>']
    return shapes, lines


def hand_group(fn, dx=0, dy=0, fill=HAND):
    shapes, lines = fn()
    s = "".join(shapes)
    out = f'<g fill="{OUTLINE}" stroke="{OUTLINE}" stroke-width="6" stroke-linejoin="round">{s}</g>'
    body = f'<g fill="{fill}">{s}</g>'
    det = (f'<g fill="none" stroke="{OUTLINE}" stroke-width="2.2" stroke-linecap="round">{"".join(lines)}</g>'
           if lines else "")
    return f'<g transform="translate({dx},{dy})">{out}{body}{det}</g>'


def stripes_board(w, h, base, stripe, n=5, r=8):
    sw = w / (2 * n)
    st = "".join(f'<rect x="{i * 2 * sw + sw:.2f}" y="0" width="{sw:.2f}" height="{h}" fill="{stripe}"/>' for i in range(n))
    return (f'<clipPath id="b"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'
            f'<g clip-path="url(#b)"><rect width="{w}" height="{h}" fill="{base}"/>{st}</g>')


def svg(title, w, h, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm">'
            f'<title>{title}</title>{inner}</svg>')


# Variante A: Tafel 150 x 200 mm, Streifen gedruckt; Hand mittig
BOARD_W, BOARD_H = 150, 200
variants = {
    "A_high-five_tafel": svg("High Five auf Streifentafel", BOARD_W, BOARD_H,
                             stripes_board(BOARD_W, BOARD_H, "#E8DBB7", "#68724D") + hand_group(high_five, 0, 10)),
    "A_peace_tafel": svg("Peace auf Streifentafel", BOARD_W, BOARD_H,
                         stripes_board(BOARD_W, BOARD_H, "#E8DBB7", "#BB3D43") + hand_group(peace, 0, 5)),
    # Variante B: nur die Hand
    "B_high-five_hand": svg("High Five – Hand", 150, 160, hand_group(high_five, 0, 0)),
    "B_peace_hand": svg("Peace – Hand", 150, 160, hand_group(peace, 0, -2)),
}
for name, content in variants.items():
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(content)
print("ok:", ", ".join(variants))
