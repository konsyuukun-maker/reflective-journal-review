#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${REFLECTIVE_JOURNAL_PYTHON:-}" ]]; then
  exec "$REFLECTIVE_JOURNAL_PYTHON" "$script_dir/save_review.py" "$@"
fi

if command -v python3 >/dev/null 2>&1 && \
  python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
  exec python3 "$script_dir/save_review.py" "$@"
fi

if command -v python >/dev/null 2>&1 && \
  python -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
  exec python "$script_dir/save_review.py" "$@"
fi

printf '%s\n' "Python 3.11 or newer is required to save a review." >&2
exit 2
