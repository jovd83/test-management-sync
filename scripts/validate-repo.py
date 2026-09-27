#!/usr/bin/env python3
"""Validate key repository invariants for this skill."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/normalized-test-case-model.md",
    "references/destination-field-matrix.md",
    "references/new-destination-research-workflow.md",
    "references/map-ids.md",
    "references/publish-results.md",
    "schemas/normalized-test-case.schema.json",
    "schemas/render-request.schema.json",
    "scripts/format-validator.py",
    "scripts/render-artifact.py",
    "scripts/scaffold-new-destination.py",
    "tests/test_format_validator.py",
    "tests/test_render_artifact.py",
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    if missing:
        print("Repository validation failed:")
        for path in missing:
            print(f"- Missing required path: {path}")
        return 1

    for schema_path in [
        root / "schemas" / "normalized-test-case.schema.json",
        root / "schemas" / "render-request.schema.json",
    ]:
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Repository validation failed: invalid JSON schema {schema_path}: {exc}")
            return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
