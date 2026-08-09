# Input resolution

## Precedence

1. Use text and files explicitly supplied for the current request.
2. If there are no explicit sources, use `journal_root` from local project instructions.
3. If neither is available, ask the user to supply material or configure a location.

Explicit sources are authoritative for that request. Do not silently add an automatic directory scan, because the same entry may appear in both places.

## Daily selection

Select material associated with the requested calendar date. A conventional local source is `YYYY-MM-DD.md`, but explicitly supplied sources may use another name. Do not include adjacent dates merely because they are in the same directory.

## Seven-day selection

The end date is inclusive. Compute the start date as six calendar days earlier and select existing, non-empty raw entries within that range. A missing day is skipped and recorded as a source gap only when that limitation matters to the interpretation.

Exclude generated reviews such as `*-SUM.md` and `*-7dSUM.md` during automatic scans. The user may explicitly provide summaries, but the review must then disclose that it is analyzing derived material rather than raw entries.

## Normalization

- Preserve chronological order.
- Retain each entry's date and any available time marker.
- Do not merge duplicate copies of the same content into separate evidence.
- Ignore files that are empty or contain only headings and whitespace.
- Treat inaccessible or unreadable sources as missing; report the limitation instead of inferring their contents.
