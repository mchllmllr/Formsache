"""Handzeichen „High Five" und „Peace" im Monoline-Stil (Einheiten: mm).

Aufbau (zwei Lagen):
  1. Linie (oben): eine durchgehende, dicke schwarze Linienzeichnung der Hand
     (Strichstärke STROKE, runde Enden), ausgeschnitten aus 3 mm schwarzem
     Acryl/Holz oder dunklem PLA. Holz schaut innerhalb der Linien durch.
  2. Basis (unten): Holzplatte = Außenkante der Linie + BASE_MARGIN, gerundet.

Konstruktion: Die Hand wird aus einfachen Formen (Handfläche, Finger,
Daumen, eingeklappte Finger) mit Ebenen-Reihenfolge aufgebaut. Die sichtbaren
Kanten dieser Formen sind die Mittellinien; sie werden mit runden Enden um
STROKE/2 gepuffert und vereinigt (shapely). So entsteht pro Lage genau eine
geschlossene Kontur ohne überlappende Grundformen.

Voraussetzung: Python 3 + shapely (pip install shapely)
Aufruf:        python3 generate.py <ausgabeordner>

Ausgabe je Zeichen <name>:
  <name>_vorschau.svg  farbige Vorschau (schwarze Linie auf Holz)
  <name>_linie.svg     Schnittkontur der Linienlage (rot = schneiden)
  <name>_basis.svg     Schnittkontur der Holzbasis (rot) + Schlüsselloch-
                       Position (blau gestrichelt, nur Markierung)
"""
import math
import sys

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

WOOD = "#D9B382"
LINE = "#1E1B19"
PAPER = "#F4F1EC"
CUT = "#FF0000"
ENGRAVE = "#0000FF"

STROKE = 7.5        # Strichstärke der schwarzen Linie
BASE_MARGIN = 7.0   # Holzrand um die Linie
INNER_R = 1.5       # Mindestradius Innenecken
MIN_GAP = 4.0       # kleinste Lücke zwischen zwei Strichen (Laser)
TARGET_H = 125.0    # Gesamthöhe der Holzbasis (Linie ca. 111 mm)
PAGE_MARGIN = 6.0
RES = 32            # Kreis-Auflösung (Segmente pro Viertelkreis)


# ---------------------------------------------------------------- Grundformen
def finger(base, angle, length, w_base, w_tip):
    """Finger als konische Kapsel. angle in Grad, 0 = senkrecht nach oben,
    positiv = nach rechts geneigt. y zeigt nach unten (SVG)."""
    bx, by = base
    a = math.radians(angle)
    tx, ty = bx + length * math.sin(a), by - length * math.cos(a)
    return unary_union([Point(bx, by).buffer(w_base / 2, RES),
                        Point(tx, ty).buffer(w_tip / 2, RES)]).convex_hull


def capsule(p0, p1, w0, w1=None):
    w1 = w0 if w1 is None else w1
    return unary_union([Point(*p0).buffer(w0 / 2, RES),
                        Point(*p1).buffer(w1 / 2, RES)]).convex_hull


def rrect(x0, y0, x1, y1, r):
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, RES)


def lines_of(g):
    if g.is_empty:
        return []
    if isinstance(g, LineString):
        return [g]
    return [p for p in getattr(g, "geoms", []) if isinstance(p, LineString)]


# ------------------------------------------------------------------ Zeichen
# Jedes Zeichen liefert: parts = [(polygon, gruppe)] in Ebenen-Reihenfolge
# (hinten -> vorne) und extra = zusätzliche Mittellinien (Fingerfugen usw.).
# Teile mit gemeinsamem Tag-Buchstaben verschmelzen (keine Kante dazwischen).

def notch(a, b):
    """Oberster Schnittpunkt zweier Umrisse = Einschnitt zwischen zwei Fingern."""
    pts = a.exterior.intersection(b.exterior)
    pts = [pts] if isinstance(pts, Point) else list(pts.geoms)
    return min(((q.x, q.y) for q in pts), key=lambda q: q[1])


def high_five():
    palm = rrect(-36, -12, 36, 50, 21)
    W = 19   # Fingerbreite (Mittellinie); Nachbarn überlappen leicht -> eine Fuge
    index = finger((-26, 2), -5, 47, W, W)
    middle = finger((-8.7, 0), -1.5, 53, W, W)
    ring = finger((8.7, 1), 1.5, 49, W, W)
    little = finger((25.5, 9), 5, 37, W - 1, W - 1)
    thumb = finger((-27, 31), -58, 28, 21, 20)
    parts = [(palm, "pf1f2f3f4t"), (little, "f4"), (ring, "f3"), (middle, "f2"),
             (index, "f1"), (thumb, "t")]
    # Daumenballen: Bogen vom Daumen-Einschnitt in die Handfläche
    x, y = notch(thumb, palm)
    extra = [arc_through((x, y), (x + 10, y + 7), (x + 13, y + 17))]
    return parts, extra


def ellipse(c, rx, ry, rot=0):
    e = affinity.scale(Point(*c).buffer(1, RES), rx, ry)
    return affinity.rotate(e, rot, origin=c)


def peace():
    # Umriss: Handfläche, V-Finger und die Knöchel der eingeklappten Finger,
    # die sich rechts aus der Hand wölben (oben größer); unten glatt rund.
    palm = rrect(-30, 0, 30, 58, 25)
    index = finger((-14, 4), -10, 43, 18.5, 18.5)
    middle = finger((5, 4), 11, 43, 18.5, 18.5)
    ring_k = Point(27, 14).buffer(10, RES)
    little_k = Point(25, 28).buffer(8, RES)
    sil = closing(unary_union([palm, index, middle, ring_k, little_k]), 6.5)
    inside = sil.buffer(-0.3, RES)
    # eingeklappte Finger als liegende Schlaufen (rechts offen in den Knöchel)
    ring = capsule((3, 12), (40, 12), 16)
    little = capsule((6, 28), (38, 28), 16)
    # Daumen: kurzer, nach oben gebogener Strich vom linken unteren
    # Handrand; runde Spitze liegt auf dem kleinen Finger. Unterkante nur
    # kurz an der Spitze -> keine geschlossene Tasche unter dem Daumen.
    axis = arc_through((-32, 49), (-16, 44), (0, 29))
    thumb = axis.buffer(9.5, RES)
    low = LineString(list(axis.coords)[:30])
    lower = max((low.offset_curve(d) for d in (9.5, -9.5)), key=lambda c: c.centroid.y)
    # auf den Umriss beschneiden: der Umriss selbst bleibt immer sichtbar
    clip = lambda g: g.intersection(sil)
    parts = [(sil, "h"), (clip(little), "l"), (clip(ring), "r"),
             (clip(thumb), "t", lower.buffer(1.0, RES))]
    return parts, []


def closing(g, r):
    return g.buffer(r, RES).buffer(-r, RES)


def arc_through(p0, p1, p2, n=40):
    """Quadratische Bézierkurve, die durch p1 verläuft."""
    cx = 2 * p1[0] - (p0[0] + p2[0]) / 2
    cy = 2 * p1[1] - (p0[1] + p2[1]) / 2
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t * t * p2[1]))
    return LineString(pts)


# ------------------------------------------------------------ Geometrie-Bau
def visible_lines(parts):
    out = []
    for i, (poly, grp, *mask) in enumerate(parts):
        # verdeckt von: späteren Teilen + Teilen mit gemeinsamem Tag
        # (Tags = einzelne Kleinbuchstaben; gemeinsamer Tag = verschmolzen)
        # optional 3. Element: Maske, deren Kanten ausgeblendet werden
        hide = [p for j, (p, g, *_) in enumerate(parts)
                if j != i and (j > i or set(g) & set(grp))]
        hide = [h.buffer(-0.01) for h in hide] + list(mask)
        line = poly.exterior
        if hide:
            line = line.difference(unary_union(hide))
        out += lines_of(line) if not isinstance(line, LineString) else [line]
    return out


def build(fn):
    parts, extra = fn()
    centre = unary_union(visible_lines(parts) + extra)
    ink = centre.buffer(STROKE / 2, RES)                 # runde Enden/Ecken
    ink = ink.buffer(INNER_R, RES).buffer(-INNER_R, RES)  # Innenecken runden
    # Holzflächen (Löcher) „öffnen": alles, was schmaler als MIN_GAP ist
    # (spitze Zwickel), wird schwarz gefüllt; Lochecken werden mit R=MIN_GAP/2
    # gerundet. Danach ist jede sichtbare Holzfläche >= MIN_GAP breit.
    polys = [ink] if isinstance(ink, Polygon) else list(ink.geoms)
    fixed, filled = [], 0
    for p in polys:
        holes = []
        for h in p.interiors:
            hp = Polygon(h)
            op = hp.buffer(-MIN_GAP / 2, RES).buffer(MIN_GAP / 2, RES)
            if op.is_empty:
                filled += 1
            else:
                holes.append(op)
        fixed.append(Polygon(p.exterior).difference(unary_union(holes)) if holes
                     else Polygon(p.exterior))
    ink = unary_union(fixed)
    solid = unary_union([Polygon(p.exterior) for p in fixed])
    base = solid.buffer(BASE_MARGIN, RES)
    base = base.buffer(8, RES).buffer(-8, RES)           # Kerben glätten
    base = Polygon(base.exterior)
    return ink, base, filled


def build_scaled(fn):
    """Skaliert die Formen so, dass die Basis TARGET_H hoch ist, ohne die
    Strichstärke zu verändern."""
    s = 1.0
    for _ in range(4):
        def scaled():
            parts, extra = fn()
            sc = lambda g: affinity.scale(g, s, s, origin=(0, 0))
            return [(sc(p), *rest) if not rest[1:] else (sc(p), rest[0], sc(rest[1]))
                    for p, *rest in parts], [sc(e) for e in extra]
        ink, base, filled = build(scaled)
        h = base.bounds[3] - base.bounds[1]
        s *= TARGET_H / h
    return ink, base, filled


def keyhole(base):
    """Schlüsselloch-Markierung für die Rückseite der Basis: Kopf Ø 9 mm,
    Schlitz 4,5 mm, 10 mm nach oben; 12 mm über dem Flächenschwerpunkt,
    damit das Schild gerade hängt. Nur Position, wird nicht geschnitten."""
    c = base.centroid
    x, y = c.x, c.y - 12
    head = Point(x, y + 4).buffer(4.5, RES)
    slot = capsule((x, y + 4), (x, y - 6), 4.5)
    return unary_union([head, slot])


# ----------------------------------------------------------------- SVG-Export
def path_d(geom):
    polys = [geom] if isinstance(geom, Polygon) else list(geom.geoms)
    d = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.simplify(0.02).coords)
            d.append("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts[:-1]) + " Z")
    return " ".join(d)


def svg(title, w, h, inner, bg=None):
    rect = f'<rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.2f}mm" height="{h:.2f}mm"><title>{title}</title>{rect}{inner}</svg>\n')


def export(name, title, fn):
    ink, base, filled = build_scaled(fn)
    key = keyhole(base)
    x0, y0, x1, y1 = base.bounds
    tx, ty = PAGE_MARGIN - x0, PAGE_MARGIN - y0
    mv = lambda g: affinity.translate(g, tx, ty)
    ink, base, key = mv(ink), mv(base), mv(key)
    w, h = x1 - x0 + 2 * PAGE_MARGIN, y1 - y0 + 2 * PAGE_MARGIN
    n_parts = 1 if isinstance(ink, Polygon) else len(ink.geoms)

    preview = (f'<path d="{path_d(base)}" fill="{WOOD}"/>'
               f'<path d="{path_d(ink)}" fill="{LINE}" fill-rule="evenodd"/>')
    cut = f'fill="none" stroke="{CUT}" stroke-width="0.1"'
    files = {
        f"{name}_vorschau.svg": svg(f"{title} – Vorschau", w, h, preview, PAPER),
        f"{name}_linie.svg": svg(f"{title} – Linie (schwarz)", w, h,
                                 f'<path d="{path_d(ink)}" {cut}/>'),
        f"{name}_basis.svg": svg(
            f"{title} – Basis (Holz)", w, h,
            f'<path d="{path_d(base)}" {cut}/>'
            f'<path d="{path_d(key)}" fill="none" stroke="{ENGRAVE}" stroke-width="0.1" '
            f'stroke-dasharray="1.5 1"><title>Schlüsselloch (Rückseite, nur Position)</title></path>'),
    }
    for fname, content in files.items():
        with open(f"{OUT}/{fname}", "w") as f:
            f.write(content)
    print(f"{name}: Basis {x1 - x0:.1f} x {y1 - y0:.1f} mm, Linienteile: {n_parts}, "
          f"Löcher: {sum(len(p.interiors) for p in ([ink] if isinstance(ink, Polygon) else ink.geoms))}, "
          f"gefüllte Engstellen: {filled}")
    return ink, base


if __name__ == "__main__":
    export("high-five", "High Five", high_five)
    export("peace", "Peace", peace)
