# Evidence

This directory stores the provenance for an extracted or generated brand manifest. It is supporting material, not a second source of normative visual values.

Recommended files:

```text
evidence/
├── sources.json
├── observations.json
├── screenshots/
│   ├── homepage-desktop.png
│   └── homepage-mobile.png
└── notes.md
```

## Provenance rules

- `sources.json` records every input URL, local path, retrieval time, access status and source type.
- `observations.json` records individual claims with a source locator, extraction method and confidence.
- Screenshots document visual observations; they do not override exact facts found in source code, CSS, font metadata or a PDF.
- Do not commit credentials, private URLs, cookies, access tokens or copyrighted source documents unless the user explicitly authorizes it.
- Record the license or usage status for every downloaded asset. Keep the original URL and a content hash when possible.

Confidence labels:

- `exact`: directly stated or extracted from source code, metadata, CSS, font files or document structure.
- `measured`: measured from a rendered page, computed style, screenshot or extracted geometry.
- `inferred`: a reasoned interpretation of visual or verbal evidence.
- `unknown`: not established by the available sources.

The normative files remain `../brand.json`, `../tokens.tokens.json` and `../DESIGN.md`.
