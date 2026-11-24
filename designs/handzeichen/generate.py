"""Erzeugt die Handzeichen-Entwürfe als SVG (Einheiten: mm).

Variante A: Holzplatte mit gedruckten Streifen (xTool) + Hand (Bambu)
Variante B: nur die Hand (Bambu)

Aufruf: python3 generate.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
OUTLINE = "#3A3A35"
HAND = "#CBC6B8"


def capsule(cx, base_y, length, width, angle):
    r = width / 2
    return (f'<rect x="{cx - r:.2f}" y="{base_y - length:.2f}" width="{width:.2f}" '
            f'height="{length:.2f}" rx="{r:.2f}" transform="rotate({angle} {cx:.2f} {base_y:.2f})"/>')


def high_five():
    shapes = [
        '<rect x="44" y="78" width="62" height="70" rx="20"/>',  # Handfläche bis Handgelenk
        capsule(52, 96, 62, 14, -10),     # Zeigefinger
        capsule(67.5, 92, 70, 14.5, -3),  # Mittelfinger
        capsule(83, 94, 64, 14, 4),       # Ringfinger
        capsule(97, 104, 48, 13, 12),     # kleiner Finger
        capsule(52, 118, 33, 16, -52),    # Daumen
    ]
    return shapes, []


def peace():
    shapes = [
        '<rect x="46" y="86" width="58" height="64" rx="20"/>',  # Handfläche bis Handgelenk
        capsule(62, 100, 70, 14.5, -16),  # Zeigefinger
        capsule(82, 100, 72, 14.5, 14),   # Mittelfinger
        '<rect x="78" y="88" width="30" height="15" rx="7.5"/>',  # Ringfinger eingeklappt
        '<rect x="80" y="102" width="27" height="14" rx="7"/>',   # kleiner Finger eingeklappt
        '<rect x="40" y="108" width="48" height="16" rx="8" transform="rotate(-12 64 116)"/>',  # Daumen
    ]
    # Nur die Trennlinien der eingeklappten Finger – ohne sie liest man das Peace-Zeichen nicht.
    lines = ['<path d="M82,103 h22"/>', '<path d="M84,117 h20"/>']
    return shapes, lines


def hand_group(fn, dx=0, dy=0, fill=HAND):
    shapes, lines = fn()
    s = "".join(shapes)
    out = f'<g fill="{OUTLINE}" stroke="{OUTLINE}" stroke-width="5" stroke-linejoin="round">{s}</g>'
    body = f'<g fill="{fill}">{s}</g>'
    det = (f'<g fill="none" stroke="{OUTLINE}" stroke-width="1.6" stroke-linecap="round">{"".join(lines)}</g>'
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
