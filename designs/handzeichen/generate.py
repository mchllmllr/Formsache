"""Erzeugt die Handzeichen-Entwürfe als SVG (Einheiten: mm).

Aufbau (zwei Lagen, Emoji-Stil):
  1. Rückenlage: Handkontur, rundum ca. 4 mm größer, dunkel (schwarzes Acryl/Holz bzw. dunkles PLA)
  2. Oberlage: Hand in Holz, Fingerdetails als Linien (Gravur bzw. Schnittfugen)

Aufruf: python3 generate.py <ausgabeordner>
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
WOOD = "#D9B382"
BACK = "#2B2724"
OFFSET = 8      # Strichstärke der Rückenlage = 2 x Randbreite (4 mm)
DETAIL = 2.6    # Linienbreite der Fingerdetails


def capsule(cx, base_y, length, width, angle):
    r = width / 2
    return (f'<rect x="{cx - r:.2f}" y="{base_y - length:.2f}" width="{width:.2f}" '
            f'height="{length:.2f}" rx="{r:.2f}" transform="rotate({angle} {cx:.2f} {base_y:.2f})"/>')


def high_five():
    shapes = [
        '<rect x="42" y="76" width="66" height="72" rx="28"/>',  # Handfläche
        capsule(53, 98, 56, 17, -11),     # Zeigefinger
        capsule(70, 94, 62, 17.5, -2),    # Mittelfinger
        capsule(87, 96, 56, 17, 6),       # Ringfinger
        capsule(101, 106, 42, 15.5, 15),  # kleiner Finger
        capsule(52, 120, 32, 19, -55),    # Daumen
    ]
    lines = [
        '<path d="M61.6,90 L60.6,74"/>',            # Fuge Zeige-/Mittelfinger
        '<path d="M78.6,90 L78.9,74"/>',            # Fuge Mittel-/Ringfinger
        '<path d="M95,96 L97.5,84"/>',              # Fuge Ring-/kleiner Finger
        '<path d="M49,108 Q55,113 57,121"/>',       # Daumenansatz
    ]
    return shapes, lines


def peace():
    shapes = [
        '<rect x="44" y="84" width="62" height="66" rx="26"/>',  # Handfläche
        capsule(63, 102, 62, 17.5, -17),  # Zeigefinger
        capsule(84, 102, 64, 17.5, 15),   # Mittelfinger
        '<rect x="78" y="88" width="32" height="17" rx="8.5"/>',  # Ringfinger eingeklappt
        '<rect x="80" y="104" width="29" height="16" rx="8"/>',   # kleiner Finger eingeklappt
        '<rect x="38" y="110" width="50" height="18" rx="9" transform="rotate(-12 63 119)"/>',  # Daumen
    ]
    lines = [
        '<path d="M84,105 h21"/>',                  # Trennung Ring-/kleiner Finger
        '<path d="M86,120 h19"/>',                  # Unterkante kleiner Finger
        '<path d="M52,122 Q66,116 80,115"/>',       # Oberkante Daumen
    ]
    return shapes, lines


def hand(fn, dx=0, dy=0, wood=WOOD, back=BACK):
    shapes, lines = fn()
    s = "".join(shapes)
    back_layer = f'<g fill="{back}" stroke="{back}" stroke-width="{OFFSET}" stroke-linejoin="round">{s}</g>'
    top_layer = f'<g fill="{wood}">{s}</g>'
    details = (f'<g fill="none" stroke="{back}" stroke-width="{DETAIL}" stroke-linecap="round">'
               f'{"".join(lines)}</g>')
    return f'<g transform="translate({dx},{dy})">{back_layer}{top_layer}{details}</g>'


def svg(title, w, h, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm">'
            f'<title>{title}</title>{inner}</svg>')


variants = {
    "high-five": svg("High Five", 150, 160, hand(high_five, 0, 0)),
    "peace": svg("Peace", 150, 160, hand(peace, 0, -2)),
    "high-five_gruen": svg("High Five – Rücken Dunkelgrün", 150, 160, hand(high_five, 0, 0, back="#4F5A38")),
    "peace_rot": svg("Peace – Rücken Weinrot", 150, 160, hand(peace, 0, -2, back="#8E2C33")),
}
for name, content in variants.items():
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(content)
print("ok:", ", ".join(variants))
