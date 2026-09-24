# Brand Manifest Template

Eine kleine, tool-agnostische Vorlage für ein Brand-Manifest-Repository. Die Vorlage trennt die **semantische Markenidentität** von den **normativen visuellen Werten**:

- `brand/brand.json` beschreibt, wer die Marke ist, wie sie spricht, welche Regeln gelten und welche Assets existieren.
- `brand/tokens.tokens.json` enthält die visuellen Werte als W3C-DTCG-Design-Tokens.
- `brand/DESIGN.md` liefert menschlich und für AI lesbare Design-Kontexte und Entscheidungen.
- `assets/` enthält die freigegebenen Dateien. Die enthaltenen Logos sind illustrative Platzhalter.

## Struktur

```text
.
├── README.md
├── Makefile
├── brand.schema.json
├── tokens.schema.json
├── brand/
│   ├── brand.json
│   ├── tokens.tokens.json
│   ├── DESIGN.md
│   └── assets/
│       ├── logo/
│       │   ├── primary.svg
│       │   ├── primary-dark.svg
│       │   ├── mark.svg
│       │   ├── wordmark.svg
│       │   └── README.md
│       ├── fonts/
│       │   ├── Inter/README.md
│       │   └── IBM-Plex-Mono/README.md
│       ├── imagery/README.md
│       ├── icons/README.md
│       ├── templates/README.md
│       └── README.md
└── scripts/
    └── validate_manifest.py
```

## Schnellstart

1. Die Beispielmarke in `brand/brand.json` durch die eigene Marke ersetzen.
2. Primitive und semantische Werte in `brand/tokens.tokens.json` anpassen.
3. Die Logo-Platzhalter durch freigegebene Assets ersetzen.
4. `brand/DESIGN.md` als kurze, konkrete Design- und AI-Anleitung bearbeiten.
5. Manifest und Referenzen prüfen:

   ```sh
   make validate
   ```

   oder direkt:

   ```sh
   python3 scripts/validate_manifest.py
   ```

Der Validator benötigt keine externen Python-Pakete. Er prüft JSON-Struktur, DTCG-Token-Referenzen, bekannte Token-Typen, Alias-Zyklen, Brand-Token-Referenzen und referenzierte Asset-Pfade.

## Regeln für die Weiterentwicklung

### Eine Quelle für visuellen Wert

`brand.json` speichert keine visuellen Farbwerte, Schriftgrößen oder Abstände. Stattdessen referenziert es DTCG-Pfade:

```json
"primary": "color.brand.primary"
```

Der Wert selbst gehört ausschließlich in `tokens.tokens.json`. Dadurch können die Markenidentität und die visuelle Oberfläche unabhängig weiterentwickelt werden.

### Semantik und Primitive trennen

- `color.brand.*` beschreibt die Farbwelt der Marke.
- `color.semantic.*` beschreibt die Bedeutung im Interface.
- `spacing.*`, `radius.*` und `border.*` sind visuelle Primitive.
- `typography.*` und `shadow.*` bündeln zusammengehörige Entscheidungen.

`color.brand.primary` und `color.semantic.primary` sollten nicht automatisch identisch sein. Die semantische Ebene darf sich ändern, ohne die Markenfarbe zu ändern.

### Keine UI-Implementierung im Manifest

Das Manifest enthält keine Buttons, CSS-Klassen, React-Komponenten oder Framework-Konfiguration. Es beschreibt Entscheidungen und referenziert Assets; die konkrete Umsetzung bleibt bei der jeweiligen Plattform.

### Assets sind Verträge

Nur freigegebene Assets unter `brand/assets/` verwenden. Dateinamen und Varianten in `brand.json` müssen mit der Asset-Struktur übereinstimmen. Bei Logos insbesondere Clear Space, Mindestgröße und Farbregeln beachten.

## AI-Kontext

Ein Agent sollte die Dateien in dieser Reihenfolge laden:

1. `brand/brand.json` für Identität, Voice, Regeln und Governance.
2. `brand/tokens.tokens.json` für alle visuellen Werte.
3. `brand/DESIGN.md` für Begründungen, Abwägungen und situative Hinweise.
4. `brand/assets/` für freigegebene Assets.

Bei einem Zielkonflikt gilt: Markenregeln zuerst, dann bestehende Tokens und Assets, danach Kontext, erst danach kreative Interpretation. Neue Farben, Schriften oder Logo-Änderungen sollten nicht stillschweigend erfunden werden.

## Anpassung

Die Datei `brand/brand.json` enthält bewusst englische Schlüsselnamen, da sie als Austauschformat und nicht als lokalisierte Oberfläche gedacht ist. Texte, Voice und Messaging können in jeder unterstützten Sprache gepflegt werden. Für mehrere Sprachvarianten können `brand.locales` erweitert und lokalisierte Dateien als Erweiterung außerhalb des Kernmanifests abgelegt werden.

Lizenz- und Nutzungsrechte für Fonts und Bilder gehören in die jeweiligen Asset-Ordner. Die Beispiel-Assets in diesem Template sind Platzhalter und sollten vor einer Veröffentlichung ersetzt werden.
