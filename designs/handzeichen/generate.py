import math, sys
OUT = sys.argv[1]
W, H = 150, 200  # Tafel in mm

def scallop_rect(x, y, w, h, r_target=7.5):
    # Bogenkante: Halbkreise nach außen entlang aller vier Seiten
    nx = max(2, round(w / (2*r_target))); ny = max(2, round(h / (2*r_target)))
    rx = w / (2*nx); ry = h / (2*ny)
    d = [f"M{x:.2f},{y:.2f}"]
    for i in range(nx):  # oben, Bögen nach oben
        d.append(f"A{rx:.2f},{rx:.2f} 0 0 1 {x+(i+1)*2*rx:.2f},{y:.2f}")
    for i in range(ny):  # rechts
        d.append(f"A{ry:.2f},{ry:.2f} 0 0 1 {x+w:.2f},{y+(i+1)*2*ry:.2f}")
    for i in range(nx):  # unten
        d.append(f"A{rx:.2f},{rx:.2f} 0 0 1 {x+w-(i+1)*2*rx:.2f},{y+h:.2f}")
    for i in range(ny):  # links
        d.append(f"A{ry:.2f},{ry:.2f} 0 0 1 {x:.2f},{y+h-(i+1)*2*ry:.2f}")
    return " ".join(d) + " Z"

def capsule(cx, cy_base, length, width, angle):
    # Finger als Kapsel: Basis (cx,cy_base), wächst nach oben, um angle Grad gedreht
    r = width/2
    return (f'<rect x="{cx-r:.2f}" y="{cy_base-length:.2f}" width="{width:.2f}" height="{length:.2f}" rx="{r:.2f}" '
            f'transform="rotate({angle} {cx:.2f} {cy_base:.2f})"/>')

def high_five():
    s = []
    s.append('<rect x="44" y="78" width="62" height="58" rx="18"/>')          # Handfläche
    s.append(capsule(52, 96, 62, 14, -10))   # Zeigefinger
    s.append(capsule(67.5, 92, 70, 14.5, -3))  # Mittelfinger
    s.append(capsule(83, 94, 64, 14, 4))     # Ringfinger
    s.append(capsule(97, 104, 48, 13, 12))   # kleiner Finger
    s.append(capsule(52, 118, 33, 16, -52))  # Daumen
    details = ['<path d="M58,118 q10,8 22,4"/>', '<path d="M86,112 q6,6 8,14"/>']
    sleeve = '<rect x="50" y="132" width="50" height="22" rx="5"/>'
    cuff_lines = ['<path d="M58,136 v14"/>','<path d="M66,136 v14"/>','<path d="M74,136 v14"/>','<path d="M82,136 v14"/>','<path d="M90,136 v14"/>']
    return s, details, sleeve, cuff_lines

def peace():
    s = []
    s.append('<rect x="46" y="86" width="58" height="52" rx="18"/>')          # Handfläche
    s.append(capsule(62, 100, 70, 14.5, -16))  # Zeigefinger
    s.append(capsule(82, 100, 72, 14.5, 14))   # Mittelfinger
    s.append('<rect x="78" y="88" width="30" height="15" rx="7.5"/>')       # Ringfinger eingeklappt
    s.append('<rect x="80" y="102" width="27" height="14" rx="7"/>')        # kleiner Finger eingeklappt
    s.append('<rect x="40" y="108" width="48" height="16" rx="8" transform="rotate(-12 64 116)"/>')  # Daumen quer
    details = ['<path d="M80,103 h24"/>', '<path d="M82,117 h22"/>', '<path d="M44,114 q20,-6 40,-6"/>']
    sleeve = '<rect x="50" y="134" width="50" height="22" rx="5"/>'
    cuff_lines = ['<path d="M58,138 v14"/>','<path d="M66,138 v14"/>','<path d="M74,138 v14"/>','<path d="M82,138 v14"/>','<path d="M90,138 v14"/>']
    return s, details, sleeve, cuff_lines

PAL = dict(wood="#E4C9A0", woodline="#C9A77A", frame="#68724D", hand="#CBC6B8", outline="#3A3A35", sleeve="#BB3D43", text="#3A3A35")

def plaque_svg(name, hand_fn, spruch, frame_col, sleeve_col):
    shapes, details, sleeve, cuff = hand_fn()
    frame = scallop_rect(9, 9, W-18, H-18, 9.5)
    inner = f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="6"/>'
    stripes = "".join(f'<rect x="{20+i*11}" y="20" width="5.5" height="{H-40}" fill="{PAL["woodline"]}" opacity=".45"/>' for i in range(10))
    hand_outline = f'<g fill="{PAL["outline"]}" stroke="{PAL["outline"]}" stroke-width="5" stroke-linejoin="round">{"".join(shapes)}</g>'
    hand_fill = f'<g fill="{PAL["hand"]}">{"".join(shapes)}</g>'
    sl_out = f'<g fill="{PAL["outline"]}" stroke="{PAL["outline"]}" stroke-width="5">{sleeve}</g>'
    sl_fill = f'<g fill="{sleeve_col}">{sleeve}</g>'
    det = f'<g fill="none" stroke="{PAL["outline"]}" stroke-width="1.6" stroke-linecap="round">{"".join(details)}</g>'
    cf = f'<g fill="none" stroke="{PAL["outline"]}" stroke-opacity=".35" stroke-width="1.4" stroke-linecap="round">{"".join(cuff)}</g>'
    txt = (f'<text x="{W/2}" y="176" text-anchor="middle" font-family="Arial Rounded MT Bold, Nunito, Arial, sans-serif" '
           f'font-weight="900" font-size="12.5" fill="{PAL["text"]}" letter-spacing=".4">{spruch}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>{name}</title>
  <!-- Ebene 1 (xTool): Rückplatte mit Bogenkante -->
  <path d="{frame}" fill="{frame_col}"/>
  <!-- Ebene 2 (xTool): Holz-Innenfläche mit gravierten Streifen -->
  <clipPath id="c"><rect x="20" y="20" width="{W-40}" height="{H-40}" rx="6"/></clipPath>
  <g fill="{PAL["wood"]}">{inner}</g><g clip-path="url(#c)">{stripes}</g>
  <!-- Ebene 3 (Bambu): Hand + Ärmel, mattes PLA -->
  <g transform="translate(0,-6)">{hand_outline}{hand_fill}{sl_out}{sl_fill}{det}{cf}</g>
  <!-- Spruch: Platzhalter-Schrift, final als Bubble Letters (Bambu) oder Gravur (xTool) -->
  {txt}
</svg>'''

open(f"{OUT}/high-five_entwurf.svg","w").write(plaque_svg("High Five – Entwurf", high_five, "GIB MIR FÜNF!", PAL["frame"], PAL["sleeve"]))
open(f"{OUT}/peace_entwurf.svg","w").write(plaque_svg("Peace – Entwurf", peace, "FRIEDEN & KEKSE", "#BB3D43", "#68724D"))
print("ok")
