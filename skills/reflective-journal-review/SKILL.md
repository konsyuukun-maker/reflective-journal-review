---
name: reflective-journal-review
description: Create evidence-grounded daily or seven-day reviews from journal entries, notes, or supplied text. Use when a user asks to summarize one day of reflections, review the seven calendar days ending on a given date, identify recurring themes or shifts in thinking, or track ideas that lack evidence of completion. Do not use for capturing or appending raw journal entries.
---

# Reflective Journal Review

Create a daily or seven-day review without inventing facts, feelings, motives, or completion states. Return Markdown by default; save it only when the user explicitly asks or local instructions define an output directory.

## Choose the mode

1. Use `daily-review` when the user asks about one specified day.
2. Use `weekly-review` when the user asks for a seven-day review. Treat the supplied end date as inclusive and analyze it plus the previous six calendar days.
3. If the request does not establish a mode, ask which review the user wants. Do not choose silently.

This skill analyzes existing material. It does not capture, append, rewrite, or reorganize raw journal entries.

## Resolve input

Read [input-resolution.md](references/input-resolution.md) before collecting sources.

- Explicitly supplied text or files take precedence. When they exist, do not also scan a configured journal directory unless the user requests both.
- Otherwise, use a `journal_root` defined by the user's local instructions and select non-empty raw entries within the review period.
- If neither source exists, ask for the entries or a configured location. Never pretend to have read inaccessible material.
- Do not use daily review files as weekly source material by default. Use raw entries unless the user explicitly chooses summaries.

Preserve source order and keep the date associated with every entry. Missing dates are absence of source material, not evidence that nothing happened.

## Apply evidence boundaries

Read [evidence-boundaries.md](references/evidence-boundaries.md) for every review. Keep four levels distinct:

1. Recorded fact or event.
2. The writer's stated judgment, feeling, or interpretation.
3. A cautious analytical inference, labeled as an observation or possibility.
4. An optional suggestion, included only when requested or clearly appropriate to the review task.

Never diagnose the writer, manufacture motives, or mark an idea or action complete without explicit evidence. Omit empty sections rather than filling a template with speculation.

## Produce the review

- For `daily-review`, read [daily-review.md](references/daily-review.md).
- For `weekly-review`, read [weekly-review.md](references/weekly-review.md).
- Follow the user's language unless they request another one.
- If the selected sources contain no substantive content, state that there is nothing to review and do not create a file.
- When citing support for an observation, prefer a short paraphrase and source date. Quote only when exact wording materially matters.

## Save only when authorized

Return the completed Markdown in the conversation by default. Save it only when the user explicitly asks or local instructions define `output_dir` as the expected destination.

Saving requires Python 3.11 or newer. Stage the complete review in a regular,
non-symlink source file, then run the command for the current platform:

```bash
# macOS or Linux: daily
python3 scripts/save_review.py daily OUTPUT_DIR YYYY-MM-DD SOURCE_FILE

# macOS or Linux: seven-day
python3 scripts/save_review.py weekly OUTPUT_DIR START_DATE END_DATE SOURCE_FILE
```

On Windows, use `py -3` in place of `python3`. The legacy
`bash scripts/save_review.sh ...` interface remains available on systems with
Bash and delegates to the same Python implementation.

The script creates a new file and refuses to overwrite an existing path. Do
not bypass that protection. If Python 3.11 or newer is unavailable, return the
review in the conversation and explain that it could not be saved. Daily
filenames are `YYYY-MM-DD-SUM.md`; weekly filenames are
`YYYY-MM-DD～MM-DD-7dSUM.md`.
