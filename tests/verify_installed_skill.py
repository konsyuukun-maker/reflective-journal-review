#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def manifest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main(arguments: list[str]) -> int:
    if len(arguments) != 2:
        print(
            "Usage: verify_installed_skill.py SOURCE_SKILL INSTALLED_SKILL",
            file=sys.stderr,
        )
        return 2

    source = Path(arguments[0])
    installed = Path(arguments[1])
    if not source.is_dir():
        print(f"Source Skill is missing: {source}", file=sys.stderr)
        return 1
    if not installed.is_dir():
        print(f"Installed Skill is missing: {installed}", file=sys.stderr)
        return 1

    source_manifest = manifest(source)
    installed_manifest = manifest(installed)
    if source_manifest != installed_manifest:
        print("Installed Skill differs from the canonical source.", file=sys.stderr)
        print(f"Source files: {sorted(source_manifest)}", file=sys.stderr)
        print(f"Installed files: {sorted(installed_manifest)}", file=sys.stderr)
        return 1

    print(f"Installed Skill matches the canonical source at {installed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
