# Handzeichen (High Five, Peace) – Strichzeichnung auf Holz

Stil: eine schwarze Linie (Mittellinie mit 5 mm Strich, runde Enden) auf einer Holzbasis,
die rundum 6,5 mm übersteht. Innenlinien laufen frei in der Handfläche aus.

```
python3 linienzeichnung.py <ausgabeordner>
```

| Datei | Inhalt |
|---|---|
| `<name>_vorschau.svg` | farbige Vorschau |
| `<name>_linie.svg` | schwarze Lage (3 mm schwarzes Acryl oder dunkles PLA) |
| `<name>_basis.svg` | Holzbasis (3 mm Sperrholz) |
| `vorschau.png` | beide Zeichen nebeneinander |

Maße in mm (viewBox = mm). Strich und Rand oben im Skript: `STROKE`, `RAND`.

**Vor dem Lasern:** Die Linien sind als Strich (stroke) angelegt. In xTool Creative Space
bzw. Inkscape einmal „Kontur in Pfad umwandeln“ und die Teile vereinigen, dann schneiden.
