# Brand Manifest

A small, tool-agnostic template for a brand-manifest repository. It separates **semantic brand identity** from **normative visual values**:

- `brand/brand.json` describes who the brand is, how it communicates, which rules apply and which assets exist.
- `brand/tokens.tokens.json` contains visual values as W3C DTCG design tokens.
- `brand/DESIGN.md` provides human- and AI-readable design context and decisions.
- `brand/assets/` contains approved files. The included logos are illustrative placeholders.
- `brand/evidence/` records sources, screenshots and the provenance of observed or derived values.

## Repository structure

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
│   ├── assets/
│   │   ├── logo/
│   │   │   ├── primary.svg
│   │   │   ├── primary-dark.svg
│   │   │   ├── mark.svg
│   │   │   ├── wordmark.svg
│   │   │   └── README.md
│   │   ├── fonts/
│   │   │   ├── Inter/README.md
│   │   │   └── IBM-Plex-Mono/README.md
│   │   ├── imagery/README.md
│   │   ├── icons/README.md
│   │   ├── templates/README.md
│   │   └── README.md
│   └── evidence/
│       └── README.md
├── scripts/
│   └── validate_manifest.py
└── skills/
    └── brand-manifest/
        ├── SKILL.md
        └── references/
            ├── manifest-contract.md
            └── source-playbook.md
```

## Quick start

1. Replace the example brand in `brand/brand.json` with your own brand.
2. Adjust primitive and semantic values in `brand/tokens.tokens.json`.
3. Replace the logo placeholders with approved assets.
4. Edit `brand/DESIGN.md` as a concise design and AI guide.
5. Validate the manifest and its references:

   ```sh
   make validate
   ```

   Or run the validator directly:

   ```sh
   python3 scripts/validate_manifest.py
   ```

The validator has no external Python dependencies. It checks JSON structure, DTCG token references, known token types, alias cycles, brand-token references and referenced asset paths. If the optional `jsonschema` package is installed, the JSON Schemas are validated as well.

## Development rules

### One source of truth for visual values

`brand.json` does not store visual color values, font sizes or spacing values. It references DTCG paths instead:

```json
"primary": "color.brand.primary"
```

The value itself belongs in `tokens.tokens.json`. This keeps brand identity and visual implementation independently evolvable.

### Separate semantics and primitives

- `color.brand.*` describes the brand's color world.
- `color.semantic.*` describes intent in an interface.
- `spacing.*`, `radius.*` and `border.*` are visual primitives.
- `typography.*` and `shadow.*` group related decisions.

`color.brand.primary` and `color.semantic.primary` do not need to be identical. The semantic layer may change without changing the brand color.

### Keep UI implementation out of the manifest

The manifest does not contain buttons, CSS classes, React components or framework configuration. It describes decisions and references assets; each platform remains responsible for implementation.

### Treat assets as contracts

Use only approved assets under `brand/assets/`. File names and variants in `brand.json` must match the asset structure. For logos, observe clear space, minimum sizes and color rules.

## AI context

An agent should load the files in this order:

1. `brand/brand.json` for identity, voice, rules and governance.
2. `brand/tokens.tokens.json` for all visual values.
3. `brand/DESIGN.md` for rationale, trade-offs and contextual guidance.
4. `brand/assets/` for approved assets.
5. `brand/evidence/` for provenance, measurements and open uncertainties.

When goals conflict, apply this order: brand rules, existing tokens and assets, contextual guidance, then creative interpretation. New colors, fonts or logo changes should never be invented silently.

## Skill: `brand-manifest`

This repository also contains the installable `brand-manifest` agent skill. It analyzes a homepage, local web project, PDF, image or other approved brand material and produces a traceable brand manifest.

### Installation

After the repository is published at `github.com/mheers/brand-manifest`, install the skill with the Skills CLI:

```sh
npx skills add mheers/brand-manifest --skill brand-manifest
```

To target OpenCode explicitly:

```sh
npx skills add mheers/brand-manifest --skill brand-manifest --agent opencode
```

List the skills available in the repository:

```sh
npx skills add mheers/brand-manifest --list
```

For local development, verify discovery with:

```sh
npx skills add . --list
```

### Usage

After installation, invoke the skill by name or through a natural-language request:

```text
/brand-manifest https://example.com ./brand
```

```text
/brand-manifest ./docs/brand-guidelines.pdf ./brand
```

```text
/brand-manifest ./reference/brand-moodboard.png ./brand
```

The skill works in five phases:

1. Identify sources, permissions and the output directory.
2. Inspect the implementation and original source: HTML, CSS, JavaScript, font files, logos, icons, metadata and PDF structure.
3. Screenshot the rendered page or document pages and measure the visual system.
4. Convert observations into `brand.json`, `tokens.tokens.json`, `DESIGN.md`, assets and evidence.
5. Validate references, schemas, assets and the final representation.

### Sources and evidence

For a homepage, implementation data is preferred: exact font families from CSS or font metadata, real logo and icon URLs, theme values, breakpoints and asset manifests. A screenshot is captured in addition to inspect spacing, hierarchy, density, style, mood, contrast and responsive variants.

For PDFs, text, metadata, embedded fonts and images are extracted and representative pages are rendered. For images, dimensions, metadata, OCR, palette and geometry are inspected. An exact font family is asserted only when metadata or an authoritative source establishes it.

Every important claim is classified in `evidence/observations.json` as `exact`, `measured`, `inferred` or `unknown`. This prevents visual guesses from being treated as documented brand facts. Asset provenance, retrieval time, hash and license status are recorded for downloaded files.

The skill creates or updates:

```text
brand/
├── brand.json
├── tokens.tokens.json
├── DESIGN.md
├── assets/
└── evidence/
    ├── sources.json
    ├── observations.json
    ├── notes.md
    └── screenshots/
```

Existing manifests are updated incrementally. Unclear identity, licensing or asset conflicts are surfaced instead of being silently overwritten. The detailed workflow and source checklists live in `skills/brand-manifest/SKILL.md` and `skills/brand-manifest/references/`.

## Customization

The keys in `brand/brand.json` are intentionally English because the file is an exchange format rather than a localized interface. Brand copy, voice and messaging can be maintained in any supported language. For multiple language variants, extend `brand.locales` and keep localized files outside the core manifest when appropriate.

Font and image licenses belong in their respective asset directories. The example assets in this template are placeholders and should be replaced before publication.
