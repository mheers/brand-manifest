#!/usr/bin/env python3
"""Validate the brand manifest and its DTCG token references.

The validator is intentionally dependency-free. If the optional ``jsonschema``
package is installed, the JSON Schemas are checked as well; the semantic checks
below always run.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRAND_PATH = ROOT / "brand" / "brand.json"
DEFAULT_TOKENS_PATH = ROOT / "brand" / "tokens.tokens.json"
BRAND_SCHEMA_PATH = ROOT / "brand.schema.json"
TOKENS_SCHEMA_PATH = ROOT / "tokens.schema.json"

ALIAS_RE = re.compile(r"\{([^{}]+)\}")
DIRECT_ALIAS_RE = re.compile(r"^\{([^{}]+)\}$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
SEMVER_RE = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
TOKEN_NAME_RE = re.compile(r"^(?!\$)[^{}.]+$")

TOKEN_TYPES = {
    "color",
    "dimension",
    "fontFamily",
    "fontWeight",
    "duration",
    "cubicBezier",
    "number",
    "strokeStyle",
    "border",
    "transition",
    "shadow",
    "gradient",
    "typography",
}
GROUP_PROPERTIES = {
    "$schema",
    "$description",
    "$type",
    "$extensions",
    "$deprecated",
    "$extends",
}
TOKEN_PROPERTIES = {
    "$value",
    "$type",
    "$description",
    "$extensions",
    "$deprecated",
    "$ref",
}
DIMENSION_UNITS = {
    "px",
    "rem",
    "em",
    "%",
    "vh",
    "vw",
    "vmin",
    "vmax",
    "ch",
    "pt",
    "mm",
    "cm",
    "in",
}
DURATION_UNITS = {"ms", "s"}


def load_json(path: Path, label: str, errors: List[str]) -> Optional[Dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        errors.append(f"{label}: file not found: {path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return None
    except OSError as exc:
        errors.append(f"{label}: cannot read {path}: {exc}")
        return None

    if not isinstance(value, dict):
        errors.append(f"{label}: top-level value must be an object")
        return None
    return value


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def is_direct_alias(value: Any) -> bool:
    return isinstance(value, str) and DIRECT_ALIAS_RE.fullmatch(value) is not None


def collect_aliases(value: Any) -> List[str]:
    aliases: List[str] = []
    if isinstance(value, str):
        aliases.extend(match.group(1).strip() for match in ALIAS_RE.finditer(value))
    elif isinstance(value, list):
        for item in value:
            aliases.extend(collect_aliases(item))
    elif isinstance(value, dict):
        for item in value.values():
            aliases.extend(collect_aliases(item))
    return aliases


def validate_name(name: str, path: str, errors: List[str]) -> None:
    if not TOKEN_NAME_RE.fullmatch(name):
        errors.append(
            f"tokens: invalid token/group name {name!r} at {path}; "
            "names may not start with '$' or contain '.', '{' or '}'"
        )


def collect_tokens(
    node: Dict[str, Any],
    parent_path: Tuple[str, ...] = (),
    inherited_type: Optional[str] = None,
    token_types: Optional[Dict[str, Optional[str]]] = None,
    aliases: Optional[Dict[str, List[str]]] = None,
    direct_aliases: Optional[Dict[str, List[str]]] = None,
    errors: Optional[List[str]] = None,
) -> Tuple[Dict[str, Optional[str]], Dict[str, List[str]], Dict[str, List[str]]]:
    """Walk a DTCG tree and collect token paths and aliases."""
    if token_types is None:
        token_types = {}
    if aliases is None:
        aliases = {}
    if direct_aliases is None:
        direct_aliases = {}
    if errors is None:
        errors = []

    current_path = ".".join(parent_path)
    if "$value" in node:
        non_properties = [key for key in node if not key.startswith("$")]
        if non_properties:
            errors.append(
                f"tokens: token {current_path!r} contains non-token child keys: {', '.join(non_properties)}"
            )
        unknown_properties = [key for key in node if key not in TOKEN_PROPERTIES]
        if unknown_properties:
            errors.append(
                f"tokens: token {current_path!r} has unknown properties: {', '.join(unknown_properties)}"
            )

        declared_type = node.get("$type", inherited_type)
        if declared_type is not None and not isinstance(declared_type, str):
            errors.append(f"tokens: token {current_path!r} has a non-string $type")
        elif declared_type is not None and declared_type not in TOKEN_TYPES:
            errors.append(
                f"tokens: token {current_path!r} uses unsupported type {declared_type!r}"
            )
        if declared_type is None:
            errors.append(
                f"tokens: token {current_path!r} needs an explicit or inherited $type"
            )

        value = node.get("$value")
        token_types[current_path] = declared_type
        references = collect_aliases(value)
        aliases[current_path] = references
        direct_aliases[current_path] = [DIRECT_ALIAS_RE.fullmatch(value).group(1)] if is_direct_alias(value) else []
        validate_token_value(current_path, value, declared_type, errors)
        return token_types, aliases, direct_aliases

    group_type = node.get("$type", inherited_type)
    if group_type is not None and not isinstance(group_type, str):
        errors.append(f"tokens: group {current_path!r} has a non-string $type")
        group_type = None
    if group_type is not None and group_type not in TOKEN_TYPES:
        errors.append(f"tokens: group {current_path!r} uses unsupported type {group_type!r}")

    for key, child in node.items():
        if key.startswith("$"):
            if key == "$root":
                if not isinstance(child, dict):
                    errors.append(f"tokens: $root at {current_path!r} must be an object")
                else:
                    collect_tokens(
                        child,
                        parent_path + (key,),
                        group_type,
                        token_types,
                        aliases,
                        direct_aliases,
                        errors,
                    )
            elif key not in GROUP_PROPERTIES:
                errors.append(f"tokens: group {current_path!r} has unknown property {key!r}")
            continue
        if not isinstance(child, dict):
            errors.append(f"tokens: group {current_path!r}.{key} must be an object")
            continue
        validate_name(key, f"{current_path}.{key}" if current_path else key, errors)
        collect_tokens(
            child,
            parent_path + (key,),
            group_type,
            token_types,
            aliases,
            direct_aliases,
            errors,
        )
    return token_types, aliases, direct_aliases


def validate_dimension(value: Any, path: str, errors: List[str], units: Set[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"tokens: {path} must be a dimension object")
        return
    if not is_number(value.get("value")):
        errors.append(f"tokens: {path}.value must be a finite number")
    unit = value.get("unit")
    if not isinstance(unit, str) or unit not in units:
        errors.append(f"tokens: {path}.unit must be one of {', '.join(sorted(units))}")


def validate_color(value: Any, path: str, errors: List[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"tokens: {path} must be a color object")
        return
    color_space = value.get("colorSpace")
    if not isinstance(color_space, str) or not color_space:
        errors.append(f"tokens: {path}.colorSpace must be a non-empty string")
    components = value.get("components")
    if not isinstance(components, list) or not components:
        errors.append(f"tokens: {path}.components must be a non-empty array")
    elif not all(is_number(component) for component in components):
        errors.append(f"tokens: {path}.components must contain finite numbers")
    if "alpha" in value and not is_number(value["alpha"]):
        errors.append(f"tokens: {path}.alpha must be a finite number")
    if "hex" in value and (not isinstance(value["hex"], str) or not HEX_RE.fullmatch(value["hex"])):
        errors.append(f"tokens: {path}.hex must be a six- or eight-digit hex color")


def validate_token_value(
    path: str,
    value: Any,
    token_type: Optional[str],
    errors: List[str],
) -> None:
    if is_direct_alias(value):
        return
    if token_type == "color":
        validate_color(value, path, errors)
    elif token_type in {"dimension", "duration"}:
        validate_dimension(value, path, errors, DIMENSION_UNITS if token_type == "dimension" else DURATION_UNITS)
    elif token_type == "fontFamily":
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"tokens: {path} must be a non-empty array of font family names")
    elif token_type == "fontWeight":
        if not (is_number(value) or isinstance(value, str)):
            errors.append(f"tokens: {path} must be a number or a string")
        elif is_number(value) and not 1 <= value <= 1000:
            errors.append(f"tokens: {path} font weight must be between 1 and 1000")
    elif token_type == "cubicBezier":
        if not isinstance(value, list) or len(value) != 4 or not all(is_number(item) for item in value):
            errors.append(f"tokens: {path} must contain four finite cubic Bézier numbers")
        elif not 0 <= value[0] <= 1 or not 0 <= value[2] <= 1:
            errors.append(f"tokens: {path} cubic Bézier x coordinates must be between 0 and 1")
    elif token_type == "number":
        if not is_number(value):
            errors.append(f"tokens: {path} must be a finite number")
    elif token_type == "typography":
        if not isinstance(value, dict):
            errors.append(f"tokens: {path} must be a typography object")
        else:
            for key in ("fontFamily", "fontSize", "fontWeight", "lineHeight"):
                if key not in value:
                    errors.append(f"tokens: {path}.{key} is required")
            for key in ("fontSize", "letterSpacing"):
                if key in value and not is_direct_alias(value[key]):
                    validate_dimension(value[key], f"{path}.{key}", errors, DIMENSION_UNITS)
            if "lineHeight" in value and not is_number(value["lineHeight"]):
                errors.append(f"tokens: {path}.lineHeight must be a finite number")
    elif token_type == "shadow":
        if not isinstance(value, list) or not value:
            errors.append(f"tokens: {path} must be a non-empty shadow array")
        else:
            for index, shadow in enumerate(value):
                shadow_path = f"{path}[{index}]"
                if not isinstance(shadow, dict):
                    errors.append(f"tokens: {shadow_path} must be an object")
                    continue
                validate_color(shadow.get("color"), f"{shadow_path}.color", errors)
                for key in ("offsetX", "offsetY", "blur", "spread"):
                    validate_dimension(shadow.get(key), f"{shadow_path}.{key}", errors, DIMENSION_UNITS)


def validate_aliases(
    token_types: Dict[str, Optional[str]],
    aliases: Dict[str, List[str]],
    direct_aliases: Dict[str, List[str]],
    errors: List[str],
) -> None:
    for source, references in aliases.items():
        for reference in references:
            if reference not in token_types:
                errors.append(f"tokens: {source} references unknown token {reference!r}")

    visited: Set[str] = set()
    reported_cycles: Set[Tuple[str, ...]] = set()

    def visit(token: str, stack: Tuple[str, ...]) -> None:
        if token in stack:
            cycle = stack[stack.index(token) :] + (token,)
            if cycle not in reported_cycles:
                reported_cycles.add(cycle)
                errors.append("tokens: circular alias detected: " + " -> ".join(cycle))
            return
        if token in visited:
            return
        visited.add(token)
        next_stack = stack + (token,)
        for target in direct_aliases.get(token, []):
            if target in token_types:
                visit(target, next_stack)

    for token in token_types:
        visit(token, ())


def path_is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_asset_path(
    brand_root: Path,
    relative_path: Any,
    label: str,
    errors: List[str],
    directory: bool = False,
) -> None:
    if not isinstance(relative_path, str) or not relative_path:
        errors.append(f"brand: {label} must be a non-empty relative path")
        return
    candidate = (brand_root / relative_path).resolve()
    if not path_is_inside(candidate, brand_root):
        errors.append(f"brand: {label} escapes the brand directory: {relative_path!r}")
        return
    if directory and not candidate.is_dir():
        errors.append(f"brand: {label} directory does not exist: {relative_path}")
    elif not directory and not candidate.is_file():
        errors.append(f"brand: {label} file does not exist: {relative_path}")


def require_token(value: Any, token_types: Dict[str, Optional[str]], label: str, errors: List[str]) -> None:
    if not isinstance(value, str) or value not in token_types:
        errors.append(f"brand: {label} must reference an existing design token; got {value!r}")


def validate_brand_assets(
    manifest: Dict[str, Any], brand_root: Path, errors: List[str]
) -> None:
    assets = manifest.get("assets", {})
    if not isinstance(assets, dict):
        return
    validate_asset_path(brand_root, assets.get("basePath"), "assets.basePath", errors, directory=True)
    for index, path in enumerate(assets.get("logo", [])):
        validate_asset_path(brand_root, path, f"assets.logo[{index}]", errors)
    for index, path in enumerate(assets.get("fonts", [])):
        validate_asset_path(brand_root, path, f"assets.fonts[{index}]", errors, directory=True)
    validate_asset_path(brand_root, assets.get("imagery"), "assets.imagery", errors, directory=True)
    validate_asset_path(brand_root, assets.get("icons"), "assets.icons", errors, directory=True)
    if "templates" in assets:
        validate_asset_path(brand_root, assets.get("templates"), "assets.templates", errors, directory=True)

    logo = manifest.get("logo", {})
    if isinstance(logo, dict):
        primary = logo.get("primary", {})
        if isinstance(primary, dict):
            validate_asset_path(brand_root, primary.get("asset"), "logo.primary.asset", errors)
        for index, variant in enumerate(logo.get("variants", [])):
            if isinstance(variant, dict):
                validate_asset_path(brand_root, variant.get("asset"), f"logo.variants[{index}].asset", errors)


def validate_brand(
    manifest: Dict[str, Any],
    brand_path: Path,
    token_types: Dict[str, Optional[str]],
    errors: List[str],
) -> None:
    required = [
        "version",
        "brand",
        "identity",
        "logo",
        "typography",
        "color",
        "imagery",
        "iconography",
        "voice",
        "content",
        "designPrinciples",
        "doDont",
        "ai",
        "assets",
        "governance",
    ]
    for field in required:
        if field not in manifest:
            errors.append(f"brand: missing required field {field!r}")
    if manifest.get("version") and not SEMVER_RE.fullmatch(str(manifest["version"])):
        errors.append("brand: version must use semantic versioning, for example 1.0.0")

    typography = manifest.get("typography", {})
    if isinstance(typography, dict):
        roles = typography.get("roles", {})
        if isinstance(roles, dict):
            for role, reference in roles.items():
                require_token(reference, token_types, f"typography.roles.{role}", errors)
        for font_key in ("primaryFont", "secondaryFont"):
            font = typography.get(font_key, {})
            if isinstance(font, dict):
                require_token(font.get("token"), token_types, f"typography.{font_key}.token", errors)

    color = manifest.get("color", {})
    if isinstance(color, dict):
        for key in ("primary", "secondary", "accent"):
            require_token(color.get(key), token_types, f"color.{key}", errors)
        semantic = color.get("semantic", {})
        if isinstance(semantic, dict):
            for key, reference in semantic.items():
                require_token(reference, token_types, f"color.semantic.{key}", errors)

    logo = manifest.get("logo", {})
    if isinstance(logo, dict):
        clear_space = logo.get("clearSpace", {})
        if isinstance(clear_space, dict):
            require_token(clear_space.get("token"), token_types, "logo.clearSpace.token", errors)
        minimum_size = logo.get("minimumSize", {})
        if isinstance(minimum_size, dict):
            for context, reference in minimum_size.items():
                if isinstance(reference, dict):
                    require_token(reference.get("token"), token_types, f"logo.minimumSize.{context}.token", errors)

    iconography = manifest.get("iconography", {})
    if isinstance(iconography, dict):
        require_token(iconography.get("strokeWidth"), token_types, "iconography.strokeWidth", errors)

    validate_brand_assets(manifest, brand_path.parent, errors)

    schema_reference = manifest.get("$schema")
    if isinstance(schema_reference, str):
        schema_path = (brand_path.parent / schema_reference).resolve()
        if not schema_path.is_file():
            errors.append(f"brand: $schema file does not exist: {schema_reference}")


def optional_schema_validation(
    instance: Dict[str, Any], schema_path: Path, label: str, errors: List[str]
) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return

    schema = load_json(schema_path, f"{label} schema", errors)
    if schema is None:
        return
    try:
        validator = jsonschema.Draft202012Validator(schema)
    except jsonschema.exceptions.SchemaError as exc:  # pragma: no cover - only a broken local schema
        errors.append(f"{label} schema: invalid schema: {exc.message}")
        return
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label} schema: {location}: {error.message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand", type=Path, default=DEFAULT_BRAND_PATH, help="path to brand.json")
    parser.add_argument("--tokens", type=Path, default=DEFAULT_TOKENS_PATH, help="path to tokens.tokens.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brand_path = args.brand.resolve()
    tokens_path = args.tokens.resolve()
    errors: List[str] = []

    manifest = load_json(brand_path, "brand.json", errors)
    token_document = load_json(tokens_path, "tokens.tokens.json", errors)
    if manifest is None or token_document is None:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    token_types, aliases, direct_aliases = collect_tokens(token_document, errors=errors)
    validate_aliases(token_types, aliases, direct_aliases, errors)
    validate_brand(manifest, brand_path, token_types, errors)
    optional_schema_validation(manifest, BRAND_SCHEMA_PATH, "brand", errors)
    optional_schema_validation(token_document, TOKENS_SCHEMA_PATH, "tokens", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Brand manifest valid: {len(token_types)} design tokens checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
