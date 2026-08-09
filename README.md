<p align="center">
  <img src="assets/readme/wordmark.svg" alt="Reflective Journal Review — Observe patterns. Understand change." width="1100">
</p>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a> · <a href="CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <a href="https://github.com/konsyuukun-maker/reflective-journal-review/actions/workflows/validate.yml"><img src="https://github.com/konsyuukun-maker/reflective-journal-review/actions/workflows/validate.yml/badge.svg" alt="Validate workflow status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-879178.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Agent%20Skill-Codex-CFA7A0.svg" alt="Agent Skill for Codex">
  <img src="https://img.shields.io/badge/Reviews-Daily%20%2B%207--day-DFCDB5.svg" alt="Daily and seven-day review modes">
</p>

<p align="center">
  <img src="assets/readme/reflection-cards.svg" alt="Three journal cards showing the Record, Reflect, and Track workflow" width="1100">
</p>

# Turn journal entries into grounded reflection.

An open-source Agent Skill that turns journal entries into evidence-grounded daily and seven-day reviews—surfacing recurring themes, shifts in thinking, and unfinished ideas without inventing a story.

Built for people who already write journals, keep Markdown notes, or practice reflective journaling and want a clearer way to observe what changes over time. The Skill works with supplied text, selected files, or an optionally configured local journal directory.

## Install

Install directly into Codex with the open Agent Skills CLI:

```bash
npx skills add konsyuukun-maker/reflective-journal-review --skill reflective-journal-review -a codex
```

Then ask Codex to use `$reflective-journal-review` with a date and the journal material you want reviewed.

<details>
<summary><strong>Manual installation</strong></summary>

Clone the repository and copy the Skill directory into your personal Codex skills directory:

```bash
git clone https://github.com/konsyuukun-maker/reflective-journal-review.git
mkdir -p ~/.codex/skills
cp -R reflective-journal-review/skills/reflective-journal-review ~/.codex/skills/
```

For repository-scoped use, place the Skill directory in the skills location used by that repository's agent configuration.

</details>

## What it helps you notice

| Notice | What the review looks for |
| --- | --- |
| **Recurring themes** | Topics, concerns, people, or questions that return across entries. |
| **Shifts in thinking** | Changes in assumptions, priorities, interpretations, or preferred next steps. |
| **Unfinished ideas** | Intentions and follow-ups that appear in the record without evidence of completion. |

The goal is not to manufacture a neat life story. It is to make the structure already present in your own words easier to see.

## See it in action

The repository includes a synthetic reading-circle journal so you can inspect the full flow without exposing anyone's private writing.

**1 · Record**

> **2026-03-10:** I want to start a neighborhood reading circle. I wrote down three possible formats but have not contacted anyone yet.

**2 · Reflect on one day**

> Two neighbor conversations moved the idea from private planning to early validation. Their preference for a monthly meeting challenged the writer's initial assumption that weekly meetings would maintain momentum.

**3 · Observe the seven-day thread**

> The idea progressed from outlining formats to testing interest and drafting an invitation. The plan became smaller and more sustainable, while choosing the first book and sending the invitation remained unfinished.

Explore the complete fictional artifacts: [source journal](examples/sample-journal.md), [daily review](examples/sample-daily-review.md), and [seven-day review](examples/sample-weekly-review.md).

## Two review modes

| Mode | Review window | Best for |
| --- | --- | --- |
| `daily-review` | One specified calendar date | Understanding the day's main themes, insights, new ideas, shifts, and open follow-ups. |
| `weekly-review` | An inclusive end date plus the previous six calendar days | Seeing cross-day patterns, important turns, progress, and ideas that still lack completion evidence. |

Missing dates are skipped rather than treated as proof that nothing happened. Daily summary files are not used as weekly input by default, which keeps the analysis grounded in the original entries.

## Grounded by evidence

Every review keeps four levels distinct:

1. **Recorded fact or event** — what the source directly says happened.
2. **The writer's own view** — a stated feeling, judgment, preference, or interpretation.
3. **Cautious observation** — an analytical inference clearly presented as an observation or possibility.
4. **Optional suggestion** — included only when requested or clearly appropriate.

The Skill does not invent motives, emotions, diagnoses, or task status. An idea remains unfinished until the record contains evidence that it was completed. Empty sections are omitted instead of being filled with speculation.

## Quick start

Daily review:

```text
Use $reflective-journal-review to review my journal for 2026-03-14.
Separate what I recorded from cautious observations, and do not invent missing context.
```

Seven-day review:

```text
Use $reflective-journal-review to create a seven-day review ending 2026-03-15
from the files I attached. Track unfinished ideas and include their first observed dates.
```

If the request does not establish a mode or provide an accessible source, the Skill asks rather than silently choosing or pretending to have read material.

## Input and saving

Input is resolved in this order:

1. Text or files explicitly supplied by the user.
2. A `journal_root` configured in local agent instructions.
3. A request for the missing journal source when neither is available.

Explicit input is not combined with an automatically discovered directory unless the user requests both. To configure local discovery, adapt [`examples/AGENTS.example.md`](examples/AGENTS.example.md) with your own paths.

Reviews return as Markdown in the conversation by default. Files are created only when the user asks or local instructions define an output directory:

- Daily: `YYYY-MM-DD-SUM.md`
- Seven-day: `YYYY-MM-DD～MM-DD-7dSUM.md`

The included save script is create-only. It rejects existing destinations, symlinks, invalid dates, empty sources, and weekly ranges other than seven calendar days.

## Development

Run the repository checks:

```bash
python3 tests/validate_structure.py
bash tests/test_save_review.sh
```

Before a release, also run OpenAI Skill Creator's `quick_validate.py` against `skills/reflective-journal-review`. Contributions should preserve the evidence boundaries and use fictional material only; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT

> If this helps you see your own patterns more clearly, star the repository so you can find it again.
