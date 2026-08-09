#!/usr/bin/env python3

import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "reflective-journal-review"
README_ASSETS = ROOT / "assets" / "readme"
WORDMARK = README_ASSETS / "wordmark.svg"
REFLECTION_CARDS = README_ASSETS / "reflection-cards.svg"
SOCIAL_PREVIEW = README_ASSETS / "social-preview.png"

EXPECTED = [
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "LICENSE",
    WORDMARK,
    REFLECTION_CARDS,
    SOCIAL_PREVIEW,
    SKILL / "SKILL.md",
    SKILL / "agents" / "openai.yaml",
    SKILL / "scripts" / "save_review.py",
    SKILL / "scripts" / "save_review.sh",
    SKILL / "references" / "input-resolution.md",
    SKILL / "references" / "evidence-boundaries.md",
    SKILL / "references" / "daily-review.md",
    SKILL / "references" / "weekly-review.md",
    ROOT / "tests" / "test_save_review.py",
    ROOT / "tests" / "test_agent_install.sh",
    ROOT / "tests" / "verify_installed_skill.py",
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

readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
readme_zh_text = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
for asset in (WORDMARK, REFLECTION_CARDS):
    relative = asset.relative_to(ROOT).as_posix()
    if f'src="{relative}"' not in readme_text:
        fail(f"README.md does not reference {relative} with a relative path")

if not re.search(r'<img\s+src="assets/readme/wordmark\.svg"\s+alt="[^"]+"', readme_text):
    fail("wordmark image must have useful alt text")
if not re.search(r'<img\s+src="assets/readme/reflection-cards\.svg"\s+alt="[^"]+"', readme_text):
    fail("reflection cards image must have useful alt text")

required_agent_ids = (
    "codex",
    "claude-code",
    "cursor",
    "gemini-cli",
    "github-copilot",
    "opencode",
)
for agent_id in required_agent_ids:
    if f"`{agent_id}`" not in readme_text:
        fail(f"README.md is missing compatibility entry for {agent_id}")
if "Agent%20Skills-Open%20Standard" not in readme_text:
    fail("README.md is missing the open Agent Skills badge")
if "开源 Codex Skill" in readme_zh_text:
    fail("README.zh-CN.md still describes the project as Codex-only")

skill_save_text = (SKILL / "scripts" / "save_review.py").read_text(encoding="utf-8")
if "os.O_EXCL" not in skill_save_text:
    fail("save_review.py must use exclusive creation for overwrite protection")
if "save_review.py" not in skill_text or "Python 3.11" not in skill_text:
    fail("SKILL.md must document the cross-platform Python saver")

for svg_path in (WORDMARK, REFLECTION_CARDS):
    try:
        ET.parse(svg_path)
    except ET.ParseError as error:
        fail(f"invalid SVG XML in {svg_path.relative_to(ROOT)}: {error}")
    svg_text = svg_path.read_text(encoding="utf-8")
    if re.search(r"<script\b", svg_text, re.IGNORECASE):
        fail(f"script element found in {svg_path.relative_to(ROOT)}")
    if re.search(r"(?:href|xlink:href)\s*=\s*['\"](?:https?:|//|data:)", svg_text, re.IGNORECASE):
        fail(f"external resource found in {svg_path.relative_to(ROOT)}")

cards_text = REFLECTION_CARDS.read_text(encoding="utf-8")
if "prefers-reduced-motion: reduce" not in cards_text:
    fail("reflection cards must support reduced motion")

png_header = SOCIAL_PREVIEW.read_bytes()[:24]
if len(png_header) != 24 or png_header[:8] != b"\x89PNG\r\n\x1a\n":
    fail("social-preview.png is not a valid PNG")
width, height = struct.unpack(">II", png_header[16:24])
if (width, height) != (1280, 640):
    fail(f"social-preview.png must be 1280x640, found {width}x{height}")
if SOCIAL_PREVIEW.stat().st_size >= 1_000_000:
    fail("social-preview.png must be smaller than 1 MB")

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
