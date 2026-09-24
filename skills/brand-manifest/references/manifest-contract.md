# Manifest Contract

Use this contract when the target repository does not already provide a schema. When a schema exists, preserve it and use this document as a semantic checklist rather than replacing the local schema.

## Files

```text
brand/
├── brand.json
├── tokens.tokens.json
├── DESIGN.md
├── assets/
│   ├── logo/
│   ├── fonts/
│   ├── imagery/
│   ├── icons/
│   └── templates/
└── evidence/
    ├── sources.json
    ├── observations.json
    ├── font-manifest.json
    ├── notes.md
    └── screenshots/
```

## `brand.json`

The manifest describes meaning, identity and governance. It should contain, when supported by evidence:

- `$schema`, `version`, `brand`, `identity`, `logo`, `typography`, `color`, `imagery`, `iconography`, `voice`, `content`, `designPrinciples`, `doDont`, `ai`, `assets` and `governance`;
- canonical name, description, URL, locales, industry and audience;
- mission, vision, values, personality and anti-personality;
- logo assets, clear space, minimum sizes and allowed/forbidden usage;
- font roles, color semantic roles, imagery guidance, icon guidance and voice rules;
- AI role, instructions, decision rules, priorities, constraints and output defaults;
- asset paths and governance metadata.

Visual values belong in the token file. Use references such as:

```json
{
  "color": {
    "primary": "color.brand.primary",
    "semantic": {
      "text": "color.semantic.text"
    }
  }
}
```

A human-readable font family, logo description or content rule can remain in `brand.json` when it is identity or asset metadata. Do not duplicate the actual font stack, color value, size or spacing value there.

## `tokens.tokens.json`

Author a DTCG-compatible token tree:

- use nested groups for organization;
- use `$type` and `$value` on tokens;
- use `{group.token}` aliases for semantic aliases;
- keep primitive values separate from semantic roles;
- use `$description` for measured, estimated or context-specific values;
- use `$extensions` only for non-standard metadata that consumers must preserve.

Minimum useful groups are:

```text
color.brand.*
color.semantic.*
color.neutral.*
font.family.*
font.weight.*
size.font.*
typography.*
spacing.*
radius.*
border.*
shadow.*
motion.*
logo.*
icon.*
```

Do not invent a complete scale when the source only proves one value. A single observed value can be represented as a named token and described as observed/estimated in evidence. Add a scale only when repeated values or an explicit system justify it.

## `DESIGN.md`

`DESIGN.md` is the explanation layer. It should state:

- the visual direction in concrete terms;
- color usage and contrast expectations;
- typography roles and hierarchy;
- spacing, layout, shape, elevation and motion principles;
- imagery and iconography direction;
- voice and content examples;
- do/don't rules;
- accessibility expectations;
- AI instructions and precedence when a request conflicts with the brand.

Use exact token paths when referring to values. Label visual interpretation as interpretation, for example: "The screenshots suggest a restrained editorial mood" rather than presenting it as a documented brand claim.

## Evidence model

`evidence/sources.json` is an array (or an object with a `sources` array) containing source records:

```json
{
  "id": "homepage",
  "kind": "web",
  "location": "https://example.com/",
  "retrievedAt": "2026-01-01T12:00:00Z",
  "access": "public",
  "owner": "Example, Inc.",
  "revision": "sha256:...",
  "notes": "Desktop and mobile screenshots"
}
```

`evidence/observations.json` is an array of fact records:

```json
{
  "id": "color.primary",
  "field": "color.primary",
  "value": "#1A4DCC",
  "status": "exact",
  "sourceId": "homepage",
  "locator": "assets/css/theme.css: --color-primary",
  "method": "stylesheet inspection",
  "notes": "Used by the primary button and wordmark"
}
```

Use these statuses consistently:

| Status | Meaning |
| --- | --- |
| `exact` | Directly stated or extracted from source code, metadata, CSS, font data or document structure. |
| `measured` | Observed from a rendered page, computed style, screenshot or extracted geometry. |
| `inferred` | A reasoned interpretation of visual or verbal evidence. |
| `unknown` | Not established by the available sources. |

Do not put a guessed value in an `exact` observation. If a field is required by the schema but unknown, ask the user or preserve the existing value and record the blocker.

## Font handoff

`evidence/font-manifest.json` is the machine-readable handoff between brand extraction and font installation. It is not a second typography token file. Each entry should contain:

```json
{
  "family": "Inter",
  "style": "Regular",
  "weight": 400,
  "files": [
    "assets/fonts/Inter/inter-regular.woff2"
  ],
  "source": "https://example.com/fonts/inter-regular.woff2",
  "license": "OFL-1.1",
  "status": "approved",
  "sha256": "...",
  "notes": "First-party webfont; verify the complete license before redistribution"
}
```

Use one of these usage statuses:

- `approved`: the intended installation or integration is permitted by the recorded license or owner approval;
- `reference-only`: useful for comparison or design reference but not approved for the requested integration;
- `unknown`: the file or rights could not be verified;
- `restricted`: the recorded terms prohibit the intended use.

Record missing metadata as unknown rather than guessing. A PDF-embedded subset is normally `reference-only` until a complete, reusable font and its rights are established.

## Asset rules

- Store only assets the user is allowed to use, or clearly mark them `reference-only`.
- Keep the original source URL/path, retrieval time, file hash, media type and license status in evidence.
- Prefer SVG for logos when an authoritative vector exists.
- Preserve font family, weight, style and license metadata.
- Use descriptive stable filenames and update every manifest reference when a filename changes.
- Do not treat a social preview, favicon or screenshot crop as a production logo without evidence and permission.

## Merge rules

When updating an existing manifest:

1. Read the existing files and validation rules first.
2. Keep valid identity and governance fields unless a higher-confidence source explicitly supersedes them.
3. Add new evidence and tokens rather than deleting unused ones by default.
4. Mark removed or contradicted fields in `evidence/notes.md`.
5. Run validation and report every unresolved conflict.

A source is not automatically more authoritative than an existing approved brand decision. Source code is authoritative for how the current implementation works; an official guideline or owner is authoritative for intended identity. Record both when they differ.

## Minimum validation checklist

- JSON parses.
- Required fields and local schema validate.
- Every `brand.json` token reference exists.
- Every token alias resolves and no alias cycle exists.
- Every asset path exists or is explicitly marked as an external/reference-only URL.
- No visual primitive is duplicated in `brand.json`.
- Evidence records cover identity claims, exact visual facts, downloaded assets and unresolved unknowns.
- Screenshots and rendered pages are named and described.
- `DESIGN.md` does not present inferred guidance as an official rule.
