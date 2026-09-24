# Acme Design System

## Overview

Acme should feel intelligent, clear and confident. The visual language is deliberately restrained. Design should communicate capability rather than decoration.

The machine-readable source of truth is `tokens.tokens.json`. The brand identity and usage rules are defined in `brand.json`.

## Design principles

1. **Clarity** — every visual element should have a clear purpose.
2. **Restraint** — use visual emphasis sparingly.
3. **Consistency** — reuse established patterns instead of inventing new ones.

## Colors

The primary blue establishes brand recognition. Use the accent orange sparingly for emphasis. The semantic color layer describes intent; it is not a replacement for the primitive palette.

Never introduce arbitrary colors. Use the semantic tokens for interface decisions and the brand tokens for identity decisions.

## Typography

Inter is the primary typeface. IBM Plex Mono is reserved for technical or data-oriented content.

Create hierarchy through size, weight and whitespace before adding decorative treatment. Avoid excessive font-size variation and do not add a third font family.

Use the named roles from `tokens.tokens.json` rather than assembling ad-hoc typography values.

## Layout

Prefer generous whitespace. Use the spacing scale in `tokens.tokens.json`; do not invent arbitrary spacing values. Establish hierarchy through alignment, grouping and contrast before adding containers or decoration.

## Imagery

Images should feel authentic and editorial. Prefer real people, natural light, a strong subject and simple backgrounds. Avoid generic stock photography, staged corporate scenes and visual clutter.

Images may use subtle brand-color accents, but should not be heavily filtered or oversaturated.

## Iconography

Use the minimal-line icon style and the shared `icon.stroke-width` token. Prefer simple, recognizable shapes. Do not mix icon families or add decorative icons without functional meaning.

## Logo usage

Use only the approved logo variants listed in `brand.json`. Maintain the `logo.clear-space` token and the minimum sizes defined by the logo tokens. Never stretch, rotate, recolor or add effects to a logo.

## Voice and content

The voice is clear, intelligent and approachable. Prefer short sentences, active voice, concrete language and specific claims. Explain benefits concretely and show real examples. Avoid corporate buzzwords, empty claims, unrealistic promises and fear-based messaging.

Adapt the tone to the context: marketing can be inspiring but restrained, documentation precise and practical, support helpful and empathetic, and technical communication direct and rigorous.

## Do's

- Use existing tokens and assets first.
- Maintain generous whitespace and a clear hierarchy.
- Keep visual emphasis purposeful and limited.
- Use real imagery where possible.
- Preserve the brand voice in generated copy.
- Check contrast and keyboard focus states.

## Don'ts

- Don't add gradients or shadows merely for decoration.
- Don't modify the logo.
- Don't introduce additional fonts or unapproved colors.
- Don't mix unrelated visual styles.
- Don't use arbitrary spacing values.
- Don't make every element visually prominent.

## AI instructions

When generating a new design or content artifact:

1. Read `brand.json` before making a brand decision.
2. Inspect `tokens.tokens.json` before choosing visual values.
3. Inspect the approved assets before generating or selecting replacements.
4. Prefer an existing token or asset over a newly invented one.
5. If a token or asset does not exist, choose the nearest established option and make the assumption explicit.
6. Follow the logo, imagery, voice and accessibility rules.
7. When a request conflicts with the brand, explain the conflict and propose a compliant alternative.
8. Do not silently change brand identity, visual primitives or governance metadata.

The order of precedence is:

1. Brand rules and constraints
2. Design tokens
3. Approved assets
4. Context-specific guidance
5. Creative interpretation

The default accessibility target is WCAG AA. A generated design must not sacrifice contrast, focus visibility or usable text sizing to satisfy an aesthetic preference.
