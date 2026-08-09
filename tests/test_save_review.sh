#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="$repo_dir/skills/reflective-journal-review/scripts/save_review.sh"
test_dir="$(mktemp -d)"
trap 'rm -rf "$test_dir"' EXIT

source_file="$test_dir/review.md"
printf '# Review\n\nSynthetic content.\n' > "$source_file"
output_dir="$test_dir/output"

daily_path="$(bash "$script" daily "$output_dir" 2026-03-14 "$source_file")"
[[ "$daily_path" == "$output_dir/2026-03-14-SUM.md" ]]
cmp -s "$source_file" "$daily_path"

if bash "$script" daily "$output_dir" 2026-03-14 "$source_file" >/dev/null 2>&1; then
  printf 'Expected overwrite protection to fail.\n' >&2
  exit 1
fi

weekly_path="$(bash "$script" weekly "$output_dir" 2026-03-09 2026-03-15 "$source_file")"
[[ "$weekly_path" == "$output_dir/2026-03-09～03-15-7dSUM.md" ]]
cmp -s "$source_file" "$weekly_path"

if bash "$script" weekly "$output_dir" 2026-03-08 2026-03-15 "$source_file" >/dev/null 2>&1; then
  printf 'Expected invalid seven-day range to fail.\n' >&2
  exit 1
fi

if bash "$script" daily "$output_dir" 2026-02-30 "$source_file" >/dev/null 2>&1; then
  printf 'Expected invalid calendar date to fail.\n' >&2
  exit 1
fi

empty_source="$test_dir/empty.md"
: > "$empty_source"
if bash "$script" daily "$output_dir" 2026-03-13 "$empty_source" >/dev/null 2>&1; then
  printf 'Expected empty source to fail.\n' >&2
  exit 1
fi

linked_source="$test_dir/linked.md"
ln -s "$source_file" "$linked_source"
if bash "$script" daily "$output_dir" 2026-03-13 "$linked_source" >/dev/null 2>&1; then
  printf 'Expected symlink source to fail.\n' >&2
  exit 1
fi

printf 'Save script tests passed.\n'
