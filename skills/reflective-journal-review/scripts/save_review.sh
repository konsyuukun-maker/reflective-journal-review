#!/usr/bin/env bash

set -euo pipefail

fail() {
  printf '%s\n' "$1" >&2
  exit 2
}

validate_date() {
  local value="$1"
  [[ "$value" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || fail "Date must use YYYY-MM-DD."

  local normalized=""
  if normalized=$(date -j -f '%Y-%m-%d' "$value" '+%Y-%m-%d' 2>/dev/null); then
    :
  elif normalized=$(date -d "$value" '+%Y-%m-%d' 2>/dev/null); then
    :
  else
    fail "Date is not a valid calendar date."
  fi
  [[ "$normalized" == "$value" ]] || fail "Date is not a valid calendar date."
}

six_days_before() {
  local value="$1"
  local calculated=""
  if calculated=$(date -j -v-6d -f '%Y-%m-%d' "$value" '+%Y-%m-%d' 2>/dev/null); then
    printf '%s\n' "$calculated"
    return
  fi
  if calculated=$(date -d "$value -6 days" '+%Y-%m-%d' 2>/dev/null); then
    printf '%s\n' "$calculated"
    return
  fi
  fail "Unable to calculate the seven-day range."
}

validate_source() {
  local value="$1"
  [[ -f "$value" && ! -L "$value" ]] || fail "Source must be a regular, non-symlink file."
  [[ -s "$value" ]] || fail "Source review is empty."
}

prepare_output_dir() {
  local value="$1"
  [[ ! -L "$value" ]] || fail "Output directory must not be a symlink."
  if [[ -e "$value" ]]; then
    [[ -d "$value" ]] || fail "Output path is not a directory."
  else
    mkdir -p -- "$value"
  fi
}

save_new_file() {
  local source_file="$1"
  local destination="$2"
  [[ ! -e "$destination" && ! -L "$destination" ]] || fail "Destination already exists; refusing to overwrite it."
  install -m 0644 "$source_file" "$destination"
  printf '%s\n' "$destination"
}

[[ $# -ge 1 ]] || fail "Expected daily or weekly operation."
operation="$1"

if [[ "$operation" == "daily" ]]; then
  [[ $# -eq 4 ]] || fail "Usage: save_review.sh daily OUTPUT_DIR YYYY-MM-DD SOURCE_FILE"
  output_dir="$2"
  review_date="$3"
  source_file="$4"
  validate_date "$review_date"
  validate_source "$source_file"
  prepare_output_dir "$output_dir"
  save_new_file "$source_file" "$output_dir/$review_date-SUM.md"
  exit 0
fi

if [[ "$operation" == "weekly" ]]; then
  [[ $# -eq 5 ]] || fail "Usage: save_review.sh weekly OUTPUT_DIR START_DATE END_DATE SOURCE_FILE"
  output_dir="$2"
  start_date="$3"
  end_date="$4"
  source_file="$5"
  validate_date "$start_date"
  validate_date "$end_date"
  [[ "$(six_days_before "$end_date")" == "$start_date" ]] || fail "START_DATE must be six calendar days before END_DATE."
  validate_source "$source_file"
  prepare_output_dir "$output_dir"
  save_new_file "$source_file" "$output_dir/${start_date}～${end_date:5:5}-7dSUM.md"
  exit 0
fi

fail "Unknown operation: $operation"
