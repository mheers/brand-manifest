# Source Playbook

Use the branch that matches the input. These are extraction procedures, not a substitute for judgment: record what the source actually exposes and label estimates.

## Common evidence protocol

For every source, create a record with:

```json
{
  "id": "homepage",
  "kind": "web",
  "location": "https://example.com/",
  "retrievedAt": "2026-01-01T12:00:00Z",
  "access": "public",
  "owner": "Example, Inc.",
  "revision": "HTML response hash or document version when available",
  "notes": "Desktop and mobile captures"
}
```

For every important fact, create an observation:

```json
{
  "id": "font.primary.family",
  "field": "typography.primaryFont.family",
  "value": "Inter",
  "status": "exact",
  "sourceId": "homepage",
  "locator": "assets/css/main.css: @font-face",
  "method": "stylesheet inspection",
  "notes": "Font source is first-party and downloadable"
}
```

Use `exact` only for direct source evidence, `measured` for rendered geometry, `inferred` for interpretation and `unknown` for gaps. Keep the locator precise enough for another analyst to reproduce the observation.

## Web homepage or web application

### 1. Inspect the implementation before judging the pixels

Use a real browser for the rendered page and source inspection for declarations. A screenshot alone cannot establish a font name, logo source or licensing status.

Collect:

- `<title>`, description, Open Graph and Twitter metadata;
- JSON-LD and other structured data;
- `link rel="icon"`, Apple touch icons, manifest icons and SVG assets;
- `<img>`, `srcset`, `picture`, CSS background images and responsive sources;
- inline SVG, sprite sheets and icon components;
- stylesheet URLs, CSS custom properties, design-token files and utility classes;
- `@font-face` declarations, `font-family`, weights, styles, font URLs and preload links;
- JavaScript bundles or source maps when they contain asset manifests or theme configuration;
- `robots.txt`, sitemap and publicly declared brand/legal pages when relevant;
- breakpoint, spacing, radius, shadow and color declarations.

With a browser, inspect the DOM, computed styles, loaded resources and network requests. If browser developer tools are unavailable, fetch the HTML and referenced CSS/assets with `webfetch` or `curl`, then search the downloaded source for the declarations. Do not infer a value from a class name when the declaration is available.

Useful read-only shell patterns include:

```sh
curl -L --fail --silent --show-error 'https://example.com/' -o /tmp/brand-homepage.html
rg -n -i 'font-face|font-family|logo|icon|stylesheet|manifest|theme-color' /tmp/brand-homepage.html
```

Resolve relative CSS, image and font URLs against the final response URL. Follow only same-origin or explicitly authorized asset hosts unless the user asks for a broader crawl.

### 2. Capture rendered states

Take a screenshot after the page reaches a stable state. Capture at least:

- a desktop viewport with the header, primary content and footer visible where practical;
- a mobile viewport or the narrowest supported layout;
- alternate states that materially affect the brand, such as an open menu, a product page or a dark mode.

For each screenshot, record viewport, device scale factor, page state, URL and capture time. Use the screenshot to assess hierarchy, whitespace, density, composition, contrast, shape language, image treatment and mood. Use computed styles or source declarations for exact values.

Do not treat a loading skeleton, cookie banner, consent overlay, error state or third-party widget as the brand's core visual language unless it is part of the intended experience.

### 3. Recover and download assets safely

Prioritize first-party assets and assets whose license is explicit. Before downloading, record:

- canonical URL or local path;
- referring HTML/CSS/component locator;
- media type and file size;
- whether the asset is a logo, icon, photograph, font or other resource;
- license or usage status;
- SHA-256 hash after download.

Use stable local names such as `logo-primary.svg`, `icon-search.svg` or `font-inter-regular.woff2`. Keep the original source URL in evidence. Do not rename a font file in a way that hides its family, weight or license. Do not copy a third-party logo merely because it appears in a search result or social preview.

A typical download-and-record flow is:

```sh
curl -L --fail --silent --show-error --output /tmp/asset.svg 'https://example.com/assets/logo.svg'
file /tmp/asset.svg
sha256sum /tmp/asset.svg
```

Validate SVG/XML and image files before copying them into `assets/`. For fonts, inspect the file metadata and retain the license. When a logo is only available as a raster screenshot, save it as a reference image and mark vector reconstruction as unknown unless an authoritative source exists.

### 4. Separate implementation facts from visual conclusions

Examples:

- `font-family: "Inter"` in a stylesheet is an exact implementation fact.
- A heading that looks like a grotesk is an inferred typeface until a declaration, font file or authoritative source identifies it.
- A repeated 24 px gap in computed styles is a measured value.
- A 24 px estimate from a screenshot is measured only if the measurement method and viewport are recorded.
- "The mood is calm and precise" is inferred language for `DESIGN.md`, not a token value.

## Local web project or source repository

1. Identify the project root and framework.
2. Read manifests, global styles, theme files, CSS variables, Tailwind/UnoCSS configuration, Storybook or component-library files, public assets and font declarations.
3. Search for SVG logos, icon libraries, image imports, `next/font`, `font-face`, design-token packages and asset manifests.
4. Run the existing development or preview command when dependencies are already available. Do not install dependencies or start destructive services without need.
5. Open the local page in a browser and capture desktop/mobile screenshots.
6. Reconcile source and render: a runtime theme, CSS variable or browser extension can change the visible result. Record both the declared and rendered values when they differ.

Exact source declarations take precedence over a screenshot. If the local project has an existing brand manifest, merge new evidence and list conflicts instead of replacing it.

## PDF or document

PDFs often contain the most reliable identity copy but may flatten or subset fonts. Inspect both structure and rendered pages.

1. Record the file hash, page count, title, author, producer, creation date and language when available.
2. Extract text with page boundaries. Use the page number and nearby heading as the locator for voice, messaging and usage rules.
3. List embedded fonts and images. A font name reported by the PDF is stronger evidence than a visual guess; a subset font still establishes the source document's declared face.
4. Render representative pages at a consistent DPI. Capture the cover, a content page, a typography specimen, a logo/asset page and a page with imagery or components.
5. Inspect color usage, page grid, margins, type scale, logo clear space and image treatment. Distinguish printed CMYK/RGB values from screen estimates.
6. Extract logos and imagery only when the document's terms permit it. Otherwise record their page/location and download only a permitted source asset.

Typical read-only tools, when installed, are `pdfinfo`, `pdftotext -layout`, `pdffonts`, `pdfimages -list` and `pdftoppm`. If a tool is unavailable, use an available PDF reader and record the limitation.

Never invent a font license from the fact that a PDF embeds a font. Preserve the document's stated terms and mark reuse unknown until verified.

## Raster or vector image

1. Inspect the original file, not only a screenshot of it. Record dimensions, format, color space/profile, DPI, metadata and file hash.
2. Run OCR for visible copy, but preserve the original wording and mark OCR corrections.
3. Sample the palette and measure repeated geometry. Keep raw samples in evidence; choose a small, intentional palette for tokens and describe the selection method.
4. Identify logos, icon families and illustration techniques visually. Crop reference regions when useful, but do not call a crop a clean production asset.
5. If the image contains no reliable font metadata or source declaration, leave the exact font name unknown. Describe observable characteristics such as weight, contrast, width and apparent classification.
6. Treat mood and style adjectives as inferred. Support them with concrete observations: palette, contrast, composition, texture, density and subject treatment.

A single image can describe a visual direction, but it cannot establish mission, legal identity, audience, licensing or complete usage rules. Ask for a homepage, guideline document or owner confirmation for those fields.

## Asset evidence and licensing

For each asset, record one of:

- `approved`: the source or owner explicitly permits the intended use;
- `reference-only`: retained for analysis but not copied into the production asset set;
- `unknown`: rights or provenance could not be established;
- `restricted`: the source terms prohibit the intended use.

An image's presence on a homepage is evidence of usage, not a license grant. Keep a short license note next to the evidence and avoid hotlinking production assets.

## When tools disagree

- Prefer source code or embedded metadata over computed style for exact names and declared values.
- Prefer a fresh browser capture over a stale cached screenshot.
- Prefer repeated measurements over a single outlier.
- Prefer the official brand/guideline source over social posts or search snippets.
- Record the disagreement and the chosen value; never erase the alternative silently.
