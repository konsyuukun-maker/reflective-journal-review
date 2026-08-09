#!/usr/bin/env bash

set -euo pipefail

[[ $# -eq 2 ]] || {
  printf '%s\n' "Usage: test_agent_install.sh AGENT_ID PROJECT_SKILLS_DIR" >&2
  exit 2
}

agent_id="$1"
project_skills_dir="$2"
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
consumer_dir="$(mktemp -d)"
trap 'rm -rf "$consumer_dir"' EXIT

(
  cd "$consumer_dir"
  npx --yes skills@1.5.22 add "$repo_dir" \
    --skill reflective-journal-review \
    --agent "$agent_id" \
    --copy \
    --yes
)

python3 "$repo_dir/tests/verify_installed_skill.py" \
  "$repo_dir/skills/reflective-journal-review" \
  "$consumer_dir/$project_skills_dir/reflective-journal-review"
