"""Erzeugt die Handzeichen-Entwürfe als SVG (Einheiten: mm).

Variante A: Acrylrahmen mit Bogenkante + Holzplatte mit gedruckten Streifen (xTool) + Holz-Hand
Variante B: nur die Hand (Bambu)

Aufruf: python3 generate.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
# Holz-Look: Hand in Holzton, dunkle Kontur (beim Lasern: Gravur bzw. beim Druck: dunkle Konturebene)
OUTLINE = "#4A3424"
HAND = "#D9B382"


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


def scallop_frame(w, h, band, r_target, color):
    """Rahmen mit Bogenkante außen und abgerundetem Innenausschnitt (Acryl, xTool)."""
    nx = max(2, round((w - 2 * r_target) / (2 * r_target)))
    ny = max(2, round((h - 2 * r_target) / (2 * r_target)))
    x0, y0, iw, ih = r_target, r_target, w - 2 * r_target, h - 2 * r_target
    rx, ry = iw / (2 * nx), ih / (2 * ny)
    d = [f"M{x0:.2f},{y0:.2f}"]
    d += [f"A{rx:.2f},{rx:.2f} 0 0 1 {x0 + (i + 1) * 2 * rx:.2f},{y0:.2f}" for i in range(nx)]
    d += [f"A{ry:.2f},{ry:.2f} 0 0 1 {x0 + iw:.2f},{y0 + (i + 1) * 2 * ry:.2f}" for i in range(ny)]
    d += [f"A{rx:.2f},{rx:.2f} 0 0 1 {x0 + iw - (i + 1) * 2 * rx:.2f},{y0 + ih:.2f}" for i in range(nx)]
    d += [f"A{ry:.2f},{ry:.2f} 0 0 1 {x0:.2f},{y0 + ih - (i + 1) * 2 * ry:.2f}" for i in range(ny)]
    outer = " ".join(d) + " Z"
    b = band + r_target
    inner = (f"M{b + 6},{b} H{w - b - 6} A6,6 0 0 1 {w - b},{b + 6} V{h - b - 6} "
             f"A6,6 0 0 1 {w - b - 6},{h - b} H{b + 6} A6,6 0 0 1 {b},{h - b - 6} V{b + 6} A6,6 0 0 1 {b + 6},{b} Z")
    return f'<path d="{outer} {inner}" fill="{color}" fill-rule="evenodd"/>'


def plaque(title, hand_fn, hy, stripe, frame_color):
    W, H, R, BAND = 170, 220, 10, 11
    off = R + BAND - 3   # Innenplatte liegt 3 mm unter dem Rahmen
    pw, ph = W - 2 * off, H - 2 * off
    panel = f'<g transform="translate({off},{off})">{stripes_board(pw, ph, "#EFE6D2", stripe, n=5, r=6)}</g>'
    return svg(title, W, H, panel + hand_group(hand_fn, 10, hy) + scallop_frame(W, H, BAND, R, frame_color))


# Variante A: Tafel 170 x 220 mm inkl. Acrylrahmen, Streifen gedruckt, Holz-Hand
variants = {
    "A_high-five_tafel": plaque("High Five – Tafel mit Rahmen", high_five, 18, "#C9D3B4", "#FF6FA8"),
    "A_peace_tafel": plaque("Peace – Tafel mit Rahmen", peace, 14, "#F3C6C0", "#FF9A3C"),
    # Variante B: nur die Hand
    "B_high-five_hand": svg("High Five – Hand", 150, 160, hand_group(high_five, 0, 0)),
    "B_peace_hand": svg("Peace – Hand", 150, 160, hand_group(peace, 0, -2)),
}
for name, content in variants.items():
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(content)
print("ok:", ", ".join(variants))
