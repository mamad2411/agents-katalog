---
name: slack-daily-signal
description: General, company-wide skill. Each day, reads every PUBLIC team-chat channel for a target date over the chat MCP and writes one structured digest per channel to signals/slack/YYYY/MM/<channel-slug>_YYYY-MM-DD.md. Public channels only — private channels and DMs are excluded by design, never read. Legal, equity, HR, NDA, and personal content is always silently excluded. Unlike the per-person email and call recaps, this is one general signal for the whole company.
owner:
  - "[[leadership]]"
creator:
  - "[[<person-slug>]]"
---

# slack-daily-signal

**Governed by** one person (the signal's standing author), not by whoever runs it.

This skill is **not per person**. Email and call recaps are per person because each inbox / calendar is private. Team chat with public-by-default channels is a **shared** source: the same thread is visible to everyone, so a per-person model would write it N times. So this skill produces **one digest per public channel per day**, with a fixed author, and runs as a single routine for the whole company.

---

## Scope: public channels only

- Reads **only** public channels. Private channels and DMs (group or 1:1) are **never enumerated, never read** — it is not a post-hoc filter, the routine simply does not request them.
- Public-by-default governs channel *visibility*. It does **not** make 1:1 correspondence on-record, and it does **not** override the company content exclusions below.
- If the company adopts a second chat system, create a sibling skill rather than expanding this one. Each skill owns one source. The output format in [`signals/slack/README.md`](../../signals/slack/) is shared.

---

## What it does

Given a target date (default: yesterday), this skill:

1. Sanity-checks prerequisites (chat MCP connected; the governing person's `people/<slug>.md` exists).
2. Loads context — in [Order of truth](../../canon/company-rules.md#order-of-truth): [`company-rules.md`](../../canon/company-rules.md), [`operations.md`](../../canon/operations.md), [`anatomy.md`](../../canon/anatomy.md), [`profile.md`](../../canon/profile.md), every team's [`canon/team/<team>.md`](../../canon/team/) (for emphasis + exclusion filters), and [`people/`](../../people/) (for participant resolution).
3. Computes the day window: `oldest` = target date 00:00, `latest` = next day 00:00, as Unix timestamps in the timezone from [`operations.md`](../../canon/operations.md) → Dates and times. Recompute every run — never hardcode.
4. Enumerates **public** channels, paginating the cursor to completion.
5. For each channel, pulls that day's messages within the window, paginating until exhausted. For every parent message with replies, pulls the full thread.
6. **Content exclusion filter runs before any synthesis** (see below). Drops or trims anything legal / equity / HR / NDA / personal.
7. Groups by **thread**: one section per material thread, all replies folded in. Drops noise: bot notifications, join/leave messages, bare-emoji reactions, automated integrations without content.
8. Decides which team(s) each channel's day impacts (`teams_impacted`).
9. Resolves participants, applying the tagging discipline from [`operations.md`](../../canon/operations.md) → "Tagging discipline at write time":
   - Internal → wiki links via `people/` matching `aliases`. Never seed internal people.
   - External → match existing `people/` / `companies/` aliases; if none, query the CRM; record found → create MD with `crm_url` and wiki-link; no record → plain text `Name, role @ company`. See [In-repo external entities](../../canon/operations.md#in-repo-external-entities--create-on-first-mention).
10. Synthesizes each section per [`signals/slack/README.md`](../../signals/slack/) → Per-thread section. Whatever a team's `canon/team/<team>.md` marks must-surface gets a bullet even when brief.
11. Assembles mandatory **frontmatter** (`author` = the governing person, `date`, `teams_impacted`, plus `related_to_*` wiki-link lists), header block, then per-thread sections. Frontmatter `teams_impacted` and body `**Team(s) impacted**` line **must agree**.
12. Writes one file per channel that had material activity to `signals/slack/YYYY/MM/<channel-slug>_YYYY-MM-DD.md`. Channels with no material activity get no file (drops are silent). Overwrites a same-channel same-date file on re-run (append-only in practice).
13. Writes the digests and any newly-created external MDs, then runs the **git write-back loop** (below).
14. Reports back: files written, channels covered, channels with no material activity (count only), action items captured, internal people linked, teams linked, external MDs created, CRM lookups with no match, git commit SHA.

---

## Content exclusion filter

Runs **before synthesis**, on every channel, regardless of the channel being public.

### Full thread drop

Drop the thread silently (no entry, no citation) if it is **entirely** any of:
- A personal / social exchange with no work content.
- Legal, equity / cap-table, HR / performance / compensation, or NDA-protected content.
- Venting or negative characterization of a colleague, a manager, or the company as a place to work.

### Segment trim

When a **work thread** contains a passing moment of the above, trim that portion and synthesize the rest normally. The trimmed portion leaves no trace — no note, no redacted marker, no count.

### What is NOT trimmed or dropped

- Legitimate **risks** or **blockers** that name a colleague factually ("the X integration is blocked pending Y's review").
- **Constructive feedback** in a retrospective / process context — keep it factual, strip emotional charge.
- **Technical or product disagreements** framed professionally — keep as "Open question / disagreement on approach" without attributing blame.

This is the company-level exclusion list from [`company-rules.md`](../../canon/company-rules.md) → "What the system MUST NEVER do", applied to chat. There is no per-person filter — this signal is general.

---

## Write-back

Writes to `main` via the **universal git loop** in [`canon/operations.md`](../../canon/operations.md) → Sync model:

1. `git pull --rebase --autostash origin main`.
2. Write the per-channel digest files plus any newly-created external `people/` / `companies/` MDs.
3. `git add` **only the specific files written in this run** — never `git add -A` or `git add .`.
4. `git commit -m "signals: chat digest <YYYY-MM-DD>"`.
5. `git push origin main`.
6. **Retry on non-fast-forward**: pull --rebase --autostash + retry, max **3 retries**. On real conflict: abort rebase, leave working copy clean, surface error.
7. **Abort cleanly on persistent failure**: no half-rebased state.

Never `git push --force`, `git reset --hard`, or history-rewriting commands on `main`.

---

## Inputs

- **Target date** (`YYYY-MM-DD`): the day the digests cover. Defaults to **yesterday** in the timezone from [`operations.md`](../../canon/operations.md) → Dates and times.

## Output destination

`signals/slack/YYYY/MM/<channel-slug>_YYYY-MM-DD.md`, one per public channel with material activity. Format in [`signals/slack/README.md`](../../signals/slack/) → Output format.

---

## Filters

Company-level exclusions plus each team's emphasis / exclusion lists, pulled at run time from:
- [`company-rules.md`](../../canon/company-rules.md) → "What the system MUST NEVER do".
- [`canon/team/<team>.md`](../../canon/team/) for any channel touching that team.

No per-person filters — this signal is general.

---

## Prerequisites

- **Chat MCP** configured in the session.
- **CRM MCP** configured — to resolve external participants via create-on-first-mention.
- The governing person's `people/<slug>.md` exists.

If any prerequisite is missing, stop and report the gap rather than producing a half-signal.

---

## How to invoke

From the repo root:

> "Run `slack-daily-signal` for yesterday."

or for a specific date:

> "Run `slack-daily-signal` for 2026-06-24."

Output goes to `signals/slack/YYYY/MM/<channel-slug>_YYYY-MM-DD.md`. Designed to run unattended on a daily schedule.

---

## Hard rules

- **Public channels only.** Never enumerate or read private channels or DMs. Never pass a user id where a channel id belongs (that reads a DM).
- **Content exclusion filter runs first, silently.** Legal / equity / HR / NDA / personal content is dropped or trimmed before synthesis. No trace, no advertised exclusion list. Default phrasing if ever surfaced: "details out of the record by design".
- **Drops are silent.** A dropped or trimmed thread leaves no trace — no "dropped" section, no footer, no per-thread note.
- Never paste full message bodies — synthesize. Material quotes only when the wording itself is the decision.
- **Never quote profanity, slurs, or blasphemy verbatim.** Chat carries off-colour language; the digest is a synthesis, so paraphrase the substance in neutral words and drop the offending language. Write-time filter on the persisted signal only — see [`company-rules.md`](../../canon/company-rules.md) → "What the system MUST NEVER do".
- Author is always the governing person. Never attribute the signal to whoever happened to run it.
- For external persons and companies, follow the **create-on-first-mention rule** ([`operations.md`](../../canon/operations.md)): query the CRM; found → MD with `crm_url` + wiki-link; not found → plain text. Never seed an external company MD without `crm_url`. Never seed internal people.
- **Apply [`canon/operations.md`](../../canon/operations.md) → Entity-scan discipline.** Scan threads for candidate entities across every entity type, fuzzy-match the global alias index, and (when run interactively) present a batched triage prompt before writing. On unattended runs, link only confident matches and report unresolved candidates.
- **Double-write every wiki-link relation pair.** See [`anatomy.md`](../../canon/anatomy.md) → Frontmatter wiki-link relations — forward + reverse pairs.
- Never duplicate the output format here — read it from [`signals/slack/README.md`](../../signals/slack/).
- Never write a digest without mandatory frontmatter (`author`, `date`, `teams_impacted`). Body `**Team(s) impacted**` must match `teams_impacted` exactly.
- Cite every thread with a permalink or `channel-id + ts`.

## When to ask the invoker

(Interactive runs only — unattended runs default conservatively and report.)
- A channel's day straddles two teams and routing is ambiguous.
- A counterparty cannot be resolved against `people/` / `companies/` and the thread carries material decisions.
- A thread sits on the edge of the exclusion filter (possible NDA / legal) — confirm before writing.
