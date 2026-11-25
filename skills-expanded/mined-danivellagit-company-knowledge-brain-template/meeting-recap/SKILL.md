---
name: meeting-recap
description: Turn a recorded meeting transcript from the team's <transcript tool> into an append-only daily-call recap signal for the day's caller. Invoke when someone asks to "recap my calls", "write up today's meetings", or after a set of recorded meetings for a given person and date.
owner:
  - "[[leadership]]"
creator:
  - "[[<person-slug>]]"
teams: []
---

# Meeting recap

**Owned by**: [canon/team/leadership.md](../../canon/team/leadership.md) (team-shared skill — any team member invokes it; behavior is parametrized by who is asking).
**Created by**: [[<person-slug>]]

## Purpose

Produce one structured, on-record recap per person per day from the recorded meetings that person attended, and write it as an append-only signal under [`signals/daily-call/`](../../signals/daily-call/). The raw recordings stay in the source tool; this skill produces the parsed, wiki-linked synthesis the rest of the graph reads.

## When to use

- A team member asks to recap their calls for a date (default: today).
- After a batch of recorded meetings, to land the day's context into the graph.

One file per person per day. Re-running for the same person and date **overwrites** the prior run — the recap is append-only across days, not across re-runs of the same day.

## Inputs

- **Source**: the team's `<transcript tool>` (e.g. Fireflies, Otter) over MCP — the recorded transcripts for the target person on the target date.
- **Who**: the person whose recap this is (resolve from `userEmail` against `aliases` in [`people/<slug>.md`](../../people/), or take it explicitly). This person becomes `author`.
- **Date**: the calendar day to recap (resolve relative dates like "today"/"yesterday" to absolute `YYYY-MM-DD`).
- **Filters at run time**: load the author's team rules ([`canon/team/<team>.md`](../../canon/team/)) and the company canon for what to emphasize and what to exclude. Do not bake per-person preferences into this team-shared file.

## Procedure / Steps

1. **Resolve who and when.** Identify the `author` person-slug and the absolute date. Determine the target file path `signals/daily-call/YYYY/MM/<person-slug>_YYYY-MM-DD.md`.
2. **Fetch transcripts.** Pull the day's recorded meetings for that person from the `<transcript tool>` over MCP. Keep the per-meeting transcript URL — it is the citation for each call.
3. **Entity-scan every meeting.** For each call, scan attendees and any named companies, systems, and themes:
   - Match people against [`people/`](../../people/) by `aliases`; internal and external. The author is not repeated in `related_to_people`.
   - For an external attendee or company with no MD, follow the create-on-first-mention rule in [`canon/operations.md`](../../canon/operations.md) -> "In-repo external entities — create-on-first-mention": query the `<CRM>`, and if a record exists create the paired MD; otherwise render as plain text.
   - A taxonomy term (system / theme / product) that already has an MD is wired as a frontmatter edge in this same write — never left as plain prose.
4. **Write the body.** One `## ` section per call, following [`signals/daily-call/README.md`](../../signals/daily-call/) -> Per-call section (Attendees, Teams touched, Key points, Decisions, Action items I own, Risks flagged, Source). Do not copy that format here — follow the link so format changes propagate. English only, regardless of the language spoken on the call. Cite every call with its transcript URL.
5. **Tag the frontmatter.** Fill the header block per [`signals/README.md`](../../signals/) -> Frontmatter: `date`, `author`, `teams_impacted`, and the `related_to_*` fields that actually appeared (omit empty arrays). Keep frontmatter and body wiki-links in sync — frontmatter is canonical for routing.
6. **Double-write bidirectional links.** `related_to_themes` is bidirectional: for each theme, also add this signal to `themes/<theme>.md -> signals:` in the same write. All other `related_to_*` fields are forward-only.
7. **Write-back.** Run the git loop below.

## Output

- **Path**: `signals/daily-call/YYYY/MM/<person-slug>_YYYY-MM-DD.md` (one per person per day).
- **Shape**: header block + one section per call. Authoritative format: [`signals/daily-call/README.md`](../../signals/daily-call/).
- Frontmatter is the routing contract; the body is human navigation. They must agree.

## Write-back

This signal is push-direct (not review-gated). Run the loop:

1. `git checkout main && git pull --rebase` — start from the latest `main`.
2. Write the recap file at the target path (create the `YYYY/MM/` folders if needed).
3. Validate markdown links before pushing, e.g. `lychee --offline --no-progress './**/*.md'` — a broken relative link blocks the push.
4. `git add` the recap (plus any paired entity MDs and any `themes/<theme>.md` reverse-link edits) and `git commit -m "signals: daily-call recap <person-slug> YYYY-MM-DD"`.
5. `git push origin main`.

Never hand-edit an existing recap and expect it to survive a re-run; re-generate or write a superseding file instead.
