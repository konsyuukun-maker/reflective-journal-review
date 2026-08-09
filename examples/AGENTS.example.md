# Reflective journal review configuration

Use `$reflective-journal-review` for daily and seven-day reviews.

- `journal_root`: `/path/to/journal`
- `output_dir`: `/path/to/reviews`
- `timezone`: `Region/City`
- Raw entry naming convention: `YYYY-MM-DD.md`
- Daily review naming convention: `YYYY-MM-DD-SUM.md`
- Seven-day review naming convention: `YYYY-MM-DD～MM-DD-7dSUM.md`

When the user explicitly supplies text or files, analyze only those sources unless they ask to combine them with `journal_root`.

Do not create a review when the selected period has no substantive entries. Do not overwrite an existing review file.

Scheduling is external to the Skill. If automations are configured, keep the daily and seven-day jobs separate and have each invoke the appropriate mode.
