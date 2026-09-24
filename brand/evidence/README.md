# Evidence

This directory stores the provenance for an extracted or generated brand manifest. It is supporting material, not a second source of normative visual values.

Recommended files:

```text
evidence/
├── sources.json
├── observations.json
├── font-manifest.json
├── font-installation.json
├── screenshots/
│   ├── homepage-desktop.png
│   └── homepage-mobile.png
└── notes.md
```

## Provenance rules

- `sources.json` records every input URL, local path, retrieval time, access status and source type.
- `observations.json` records individual claims with a source locator, extraction method and confidence.
- `font-manifest.json` is the handoff from brand analysis to the `brand-fonts` skill. It contains font files, metadata, sources, checksums and usage status.
- `font-installation.json` is written after a `brand-fonts` run and records the target, files changed and validation results.
- Screenshots document visual observations; they do not override exact facts found in source code, CSS, font metadata or a PDF.
- The skill invocation is treated as owner authorization for copying ordinary public or first-party assets. Do not commit credentials, private URLs, cookies, access tokens or unnecessary copyrighted source documents.
- Record the license or usage status for every downloaded asset. Keep the original URL and a content hash when possible.

Confidence labels:

- `exact`: directly stated or extracted from source code, metadata, CSS, font files or document structure.
- `measured`: measured from a rendered page, computed style, screenshot or extracted geometry.
- `inferred`: a reasoned interpretation of visual or verbal evidence.
- `unknown`: not established by the available sources.

For asset usage, `owner-provided` means the file was copied under the owner-invocation scope without an independently verified production license. It is not the same as `approved`.

The font handoff uses entries such as:

```json
{
  "family": "Inter",
  "style": "Regular",
  "weight": 400,
  "files": ["assets/fonts/Inter/inter-regular.woff2"],
  "source": "https://example.com/fonts/inter-regular.woff2",
  "authorization": "owner-invocation",
  "license": "OFL-1.1",
  "status": "approved",
  "sha256": "..."
}
```

The normative files remain `../brand.json`, `../tokens.tokens.json` and `../DESIGN.md`.
