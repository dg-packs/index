#!/usr/bin/env python3
"""Checks index.json: python3 check.py [file]. Exits non-zero and names each problem."""
import json
import re
import sys

SIMPLE_ID = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
RESERVED = {"all", "node", "kind", "tag", "children", "descendants", "edge_kind", "port", "row", "lift", "generic"}
SOURCE = re.compile(r"^(https://|ssh://)?[^/\s:]+\.[^/\s]+(//?[^/\s]+)+$")
FIELDS = ["name", "source", "description", "license"]


def problems(index: object) -> list[str]:
    if not isinstance(index, dict) or set(index) != {"version", "packs"}:
        return ['the file must be an object holding "version" and "packs" alone']
    if index["version"] != 1:
        return [f'"version" must be 1, not {index["version"]!r}']
    if not isinstance(index["packs"], list):
        return ['"packs" must be a list']
    found = []
    names = []
    for i, pack in enumerate(index["packs"]):
        at = f"pack {i + 1}"
        if not isinstance(pack, dict) or sorted(pack) != sorted(FIELDS):
            found.append(f"{at}: must hold exactly {', '.join(FIELDS)}")
            continue
        at = f"pack {pack['name']!r}"
        for field in FIELDS:
            value = pack[field]
            if not isinstance(value, str) or not value.strip() or not value.isprintable():
                found.append(f"{at}: {field} must be printable text on one line")
                break
        else:
            name, source = pack["name"], pack["source"]
            if not SIMPLE_ID.match(name) or name in RESERVED:
                found.append(f"{at}: the name must be a simple ID and not a reserved word")
            if not SOURCE.match(source):
                found.append(f"{at}: the source must be <host>/<path>, or an https:// or ssh:// URL")
            elif source.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1] != name:
                found.append(f"{at}: the name must be the source's last segment, which becomes the pack's local name")
            names.append(name)
    if names != sorted(names):
        found.append("packs must be sorted by name")
    if len(names) != len(set(names)):
        found.append("two packs have one name")
    return found


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "index.json"
    try:
        with open(path, encoding="utf-8") as f:
            found = problems(json.load(f))
    except (OSError, ValueError) as e:
        found = [str(e)]
    for problem in found:
        print(f"{path}: {problem}", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
