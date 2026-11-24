# Handzeichen (High Five, Peace) – Monoline-Stil

Zwei Lagen: schwarze Linienzeichnung (3 mm schwarzes Acryl/Holz oder dunkles PLA)
auf einer Holzbasis, die die Linie rundum mit ca. 7 mm Holzrand einfasst.

**Voraussetzung:** Python 3 + [shapely](https://pypi.org/project/Shapely/) (`pip install shapely`)

```
python3 generate.py <ausgabeordner>
```

| Datei | Inhalt |
|---|---|
| `<name>_vorschau.svg` | farbige Vorschau (Linie #1E1B19 auf Holz #D9B382) |
| `<name>_linie.svg` | Schnittkontur der schwarzen Linienlage – **ein** zusammenhängendes Teil, rot = schneiden |
| `<name>_basis.svg` | Schnittkontur der Holzbasis (rot) + Schlüsselloch-Position (blau gestrichelt, nur Markierung) |
| `vorschau.png` | beide Zeichen nebeneinander (Playwright, deviceScaleFactor 2) |

Maße: Basis 125 mm hoch (High Five 112 mm, Peace 88 mm breit), Linie 7,5 mm,
Holzlücken innerhalb der Linie überall ≥ 4 mm, Innenecken R ≥ 1,5 mm.
Alle Maße stehen oben in `generate.py` (STROKE, BASE_MARGIN, MIN_GAP, TARGET_H).
