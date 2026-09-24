# Font Installation Targets

Use only the section for the selected target. Commands are examples; adapt paths to the user's machine and project.

## Metadata inspection

Prefer a font-aware tool over guessing from filenames:

```sh
fc-scan --format '%{family}\n%{style}\n%{weight}\n%{fontversion}\n' path/to/font.woff2
```

When `fontTools` is available, inspect the font tables and names with `ttx` or a short read-only Python script. Record at least:

- family and subfamily;
- full name and PostScript name;
- weight and style;
- variable-font axes;
- format and file size;
- embedding/subsetting flags where available;
- SHA-256 checksum.

A filename such as `brand-font.woff2` is not evidence that the family is `Brand Font`.

## Web projects

### Before changing the project

1. Identify the framework and CSS entry point.
2. Search for existing `@font-face`, `next/font`, `fontsource`, CSS variables, font packages and public asset paths.
3. Check whether the project already loads the exact family and weights.
4. Preserve the project's build and deployment conventions.

### Integration pattern

A minimal declaration has this shape:

```css
@font-face {
  font-family: "Brand Sans";
  src: url("/fonts/brand-sans-regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Use one declaration per real family/style/weight combination. Keep the source font file in the project's public or source asset directory according to its existing conventions. Do not install an operating-system copy merely to make a web build work.

### Validation

- run the project's existing typecheck/build or a focused CSS check;
- load the page in a browser;
- inspect the network request and computed `font-family`;
- verify that the intended glyphs and weights render;
- check the fallback while the webfont loads;
- record the changed files in `font-installation.json`.

## Linux system installation

Use a per-user installation by default:

```sh
mkdir -p "$HOME/.local/share/fonts/brand-manifest"
cp --preserve=timestamps path/to/font.woff2 "$HOME/.local/share/fonts/brand-manifest/"
fc-cache -f "$HOME/.local/share/fonts"
fc-match "Brand Sans"
```

Do not use `sudo` without an explicit user request. Keep the original file and checksum. If a font is already installed, compare metadata and checksum before replacing anything.

## macOS system installation

Use the user's font directory:

```sh
mkdir -p "$HOME/Library/Fonts/brand-manifest"
cp path/to/font.woff2 "$HOME/Library/Fonts/brand-manifest/"
```

Use Font Book or the target application to verify that the family is available. Do not claim success from the copy command alone.

## Windows system installation

Use the current user's font directory and preserve the original filename. Verify the installed family through the target application or Windows font APIs. Do not silently replace an existing family with the same name but different metadata.

## Design-tool staging

When a hosted design tool cannot be automated reliably:

1. create a staging directory such as `brand/evidence/font-staging/` or a user-selected design-assets folder;
2. copy only approved font files;
3. write an inventory with family, style, weight, source, license and checksum;
4. provide the staging path and manual import instructions;
5. record the result as `staged`, not `installed`, unless an actual import was verified.

## Failure handling

- Missing file: stop that font and keep the rest of the report.
- Invalid or unsupported format: preserve the source and explain the accepted alternatives.
- License unknown/restricted: stage for review or skip; do not integrate.
- Family metadata mismatch: report the mismatch and ask which identity is authoritative.
- Existing system font with the same name: do not overwrite without explicit confirmation.
- Build or font-query failure: remove only files created by this run when safe, then report the failure.
