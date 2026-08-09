# Contributing

Contributions are welcome when they preserve the project's evidence boundaries and do not introduce personal journal material.

## Workflow

1. Create a focused branch from `main`.
2. Update the Skill, references, tests, and changelog together when behavior changes.
3. Run `python3 tests/validate_structure.py` and `bash tests/test_save_review.sh`.
4. Run OpenAI Skill Creator's `quick_validate.py` against the Skill directory.
5. Open a pull request describing observable behavior changes and evidence-boundary implications.

## Versioning

- Patch releases clarify rules or fix compatible behavior.
- Minor releases add compatible inputs, modes, or output capabilities.
- Major releases change established invocation, input precedence, evidence boundaries, or output contracts.

Never add real journal entries, private paths, account identifiers, access tokens, or copied conversations to examples or tests.
