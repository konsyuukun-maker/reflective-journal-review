# Changelog

All notable changes are documented here. This project follows Semantic Versioning.

## [0.2.0] - 2026-08-09

### Added

- CI-verified installation for Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, and OpenCode.
- A Python 3.11+ create-only save implementation for macOS, Linux, and Windows.
- Cross-platform save tests, concurrent-write coverage, and open Agent Skills specification validation.

### Changed

- Repositioned the project as one standards-based Skill shared across compatible agents.
- Kept the Bash save command as a compatibility wrapper around the Python implementation.
- Updated English and Chinese documentation with agent-neutral prompts and compatibility boundaries.

## [0.1.0] - 2026-08-09

### Added

- Evidence-grounded `daily-review` and `weekly-review` modes.
- Explicit-input-first source resolution with optional local Markdown discovery.
- Create-only saving for daily and seven-day Markdown reviews.
- Synthetic examples, structural validation, shell tests, and continuous integration.
