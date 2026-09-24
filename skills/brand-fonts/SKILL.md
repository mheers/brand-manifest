---
name: brand-fonts
description: Install or integrate approved fonts from a brand manifest into a web project, a local operating system, or a design-tool staging directory. Use when someone asks to install, register, package, or wire up fonts discovered by brand-manifest.
argument-hint: "<brand-directory> --target <web|system|design> [options]"
---

# Brand Fonts

Install or integrate fonts from a brand repository without losing provenance, metadata or license boundaries. This skill consumes the handoff produced by `brand-manifest` and keeps installation separate from brand analysis.

`$ARGUMENTS` contains a brand directory, a required target and optional target-specific paths. If the target is missing, ask for it. Never silently default to operating-system installation.

## Safety boundary

- Read `brand/evidence/font-manifest.json` first. If it is absent or empty, inspect `brand/brand.json` and `brand/assets/fonts/`, create the handoff, and mark derived entries as provisional.
- Install only fonts whose usage status is `approved`, unless the user explicitly confirms a different legally permitted action.
- Keep `reference-only`, `unknown` and `restricted` fonts out of system and production web integration. Stage them for review when useful.
- A font downloaded from a webpage is not automatically redistributable. Preserve its source URL, license and checksum.
- Treat PDF-embedded or subset fonts as reference material unless the user confirms that the complete font and redistribution rights are available.
- Copy files; do not move or rename the originals. Preserve family, style, weight and metadata in filenames and reports.
- Do not use `sudo` or modify system-wide directories when a per-user installation is available.
- Do not install a font into Figma, Adobe or another hosted tool without an explicit user request and an available supported integration path.

## Output contract

The skill writes an installation report to:

```text
<brand-directory>/evidence/font-installation.json
```

The report contains the selected target, source files, license status, checksums, actions taken, validation results and any unresolved warnings. For a web project, generated CSS and copied font files belong in that project. For a system installation, record the per-user destination. For design tooling, use a clearly named staging directory unless the user specifies another output.

## Phase 0 — Resolve inputs and target

1. Resolve the brand directory and confirm that `brand/brand.json`, the evidence handoff and font assets are readable.
2. Read the target project's existing font configuration before changing it.
3. Select exactly one target unless the user explicitly requests a staged web font plus a system install.
4. Establish the output location and whether existing files may be replaced.
5. For `system` and `design` targets, obtain explicit confirmation before copying into the destination.

**Done when:** the source fonts, target, destination, license boundary and overwrite policy are explicit.

## Phase 1 — Inventory and classify fonts

1. Read every handoff entry and resolve its file path relative to the brand directory.
2. Validate that each file exists, is a supported font format and has a stable checksum.
3. Inspect metadata with available tools such as `fontTools`/`ttx`, `fc-scan` or `otfinfo`. Record family, subfamily, full name, PostScript name, weight, style, format, axes and embedding restrictions.
4. Compare the metadata with the handoff and the typography fields in `brand.json`. Treat a mismatch as a conflict to report, not as a reason to rewrite metadata silently.
5. Check the license and usage status. Mark incomplete, subsetted or unverifiable fonts as `reference-only` or `unknown`.
6. Create or update `evidence/font-manifest.json` when the handoff is missing or incomplete. Use `inferred` or `provisional` notes for facts that are not directly established by the source.

**Done when:** every candidate font has a file, checksum, metadata record, license status and integration decision.

## Phase 2 — Apply the selected target

Read `references/platforms.md` for the target-specific procedure.

### Web target

- Inspect the project's framework, build pipeline, CSS entry points and existing font declarations.
- Prefer local `@font-face` integration over installing a font into the operating system.
- Copy the smallest appropriate web formats, normally WOFF2, while retaining an approved original when the project needs it.
- Use the exact family, weight and style metadata; do not collapse weights into a misleading single family.
- Add `font-display` and a deliberate fallback stack. Preserve existing font loading if it already satisfies the manifest.
- Update the project's integration manifest or report the exact files changed. Do not change the brand's canonical font family merely to match a local alias.

### System target

- Ask for confirmation immediately before writing to the font destination.
- Prefer the current user's font directory: `~/.local/share/fonts/` on Linux, `~/Library/Fonts/` on macOS, or the current user's Windows font directory.
- Copy only approved files, retain original names, refresh the platform cache when appropriate, and verify the installed family with a platform font query.
- Do not uninstall, overwrite or remove existing fonts automatically.
- Report the exact destination and provide a manual removal note when the user needs one.

### Design target

- Create a staging directory with the approved font files, a checksum manifest and a human-readable inventory.
- Do not claim that a hosted design tool has installed a font when only a local staging copy was created.
- Use a supported API or an explicit manual import flow when one is available; otherwise provide the staging path and import instructions.

**Done when:** the selected target contains the approved font files or a clearly documented staging result, and no unapproved file was installed.

## Phase 3 — Verify the integration

For every target:

- confirm the copied file hash matches the source;
- verify that the family, style and weight resolve as expected;
- check that the web build, font query or design-tool import reports no errors;
- inspect a rendered page or sample document when the target affects rendering;
- preserve the source handoff and write `evidence/font-installation.json`.

If validation fails, leave the source repository unchanged where possible, report the failing file and stop the affected target. Do not make a font appear installed by changing only a name or CSS variable.

## Phase 4 — Report

Give the user:

- the target and destination;
- installed, copied or staged files;
- family/style/weight metadata;
- license and source status;
- commands or project files changed;
- validation results and warnings;
- fonts intentionally skipped and the reason.

Use `evidence/font-installation.json` for the durable record and keep the user-facing report concise.

## Completion checklist

- [ ] `font-manifest.json` was read or created.
- [ ] Every font has metadata, checksum, source and license status.
- [ ] Only approved fonts were installed or integrated.
- [ ] The target was explicit and existing configuration was inspected first.
- [ ] Web, system or design-specific validation passed.
- [ ] The installation report and remaining warnings are written.
