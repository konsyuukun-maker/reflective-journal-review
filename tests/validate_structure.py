#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "reflective-journal-review"

EXPECTED = [
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "LICENSE",
    SKILL / "SKILL.md",
    SKILL / "agents" / "openai.yaml",
    SKILL / "scripts" / "save_review.sh",
    SKILL / "references" / "input-resolution.md",
    SKILL / "references" / "evidence-boundaries.md",
    SKILL / "references" / "daily-review.md",
    SKILL / "references" / "weekly-review.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


for path in EXPECTED:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
frontmatter = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
if not frontmatter:
    fail("SKILL.md has invalid frontmatter delimiters")

header = frontmatter.group(1)
if not re.search(r"^name: reflective-journal-review$", header, re.MULTILINE):
    fail("SKILL.md has an unexpected name")
if not re.search(r"^description: .+", header, re.MULTILINE):
    fail("SKILL.md is missing a description")
if "[TODO" in skill_text:
    fail("SKILL.md still contains template TODO text")

openai_yaml = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
if "$reflective-journal-review" not in openai_yaml:
    fail("default_prompt must mention the Skill by name")

private_markers = [
    "/" + "Users" + "/",
    "g-" + "p-",
    "35aa" + "31e4",
]
email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path == Path(__file__).resolve():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for marker in private_markers:
        if marker in text:
            fail(f"private marker found in {path.relative_to(ROOT)}")
    if email_pattern.search(text):
        fail(f"email address found in {path.relative_to(ROOT)}")

print("Structure and privacy checks passed.")
