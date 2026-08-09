# Reflective Journal Review

`reflective-journal-review` is an open-source Codex Skill for evidence-grounded reflection over one day or seven consecutive calendar days. It works with supplied text, selected files, or an optionally configured Markdown journal directory.

The Skill summarizes what was recorded, surfaces recurring themes and shifts in thinking, and tracks ideas without pretending that silence means completion. It does not capture raw journal entries and does not create scheduled tasks.

## Modes

- `daily-review` analyzes one specified calendar date.
- `weekly-review` analyzes an inclusive end date plus the preceding six calendar days.

Both modes separate recorded facts, the writer's own views, cautious analytical observations, and optional suggestions. Empty sections are omitted, and no review is created when there is no substantive input.

## Install

Clone the repository, then copy or link the Skill directory into your personal Codex skills directory:

```bash
git clone https://github.com/konsyuukun-maker/reflective-journal-review.git
mkdir -p ~/.codex/skills
cp -R reflective-journal-review/skills/reflective-journal-review ~/.codex/skills/
```

For a repository-scoped installation, place the Skill directory in the skills location used by that repository's agent configuration.

## Use

Examples:

```text
Use $reflective-journal-review to review my journal for 2026-03-14.

Use $reflective-journal-review to create a seven-day review ending 2026-03-15
from the files I attached.
```

Explicitly supplied text or files take precedence over automatic directory discovery. If you want automatic local discovery, adapt [`examples/AGENTS.example.md`](examples/AGENTS.example.md) with your own `journal_root`. The default response is Markdown in the conversation; file creation occurs only when requested or when local instructions define an output directory.

## Output files

- Daily: `YYYY-MM-DD-SUM.md`
- Seven-day: `YYYY-MM-DD～MM-DD-7dSUM.md`

The included save script is create-only. It rejects existing destinations, symlinks, invalid dates, empty sources, and weekly ranges other than seven calendar days.

## Development

Run the repository checks:

```bash
python3 tests/validate_structure.py
bash tests/test_save_review.sh
```

Before a release, also run OpenAI's Skill Creator `quick_validate.py` against `skills/reflective-journal-review`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the versioning workflow.

## License

MIT
