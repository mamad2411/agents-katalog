---
description: Process my rants. Say "process my rants" or "dream on the rants" (or run /founder-os:dream). Distils unprocessed rants into a 5-line digest and updates patterns, flags, parked decisions, needs-input, client signals, and proposed working preferences as warranted.
---

# Dream

Process all unprocessed rants in `brain/rants/`. Distil what surfaced. Write a tight 5-line digest. Hard cap on output. The user will not read more than 5 lines.

## Procedure

1. Walk `brain/rants/`. For each file, parse entries by frontmatter. Collect every entry where `processed: false`.

2. For each unprocessed entry, classify what it contains and stamp every new entry with a stable ID per `rules/entry-conventions.md`:
   - **Pattern** - recurring theme, observation, framework. Append to `brain/patterns.md` with a stamped `pattern-YYYY-MM-DD-NNN` ID.
   - **Flag** - stall, frustration, role feedback, friction. Append to `brain/flags.md` with `Status: **OPEN.**` and Severity Week 1 unless escalation is obvious. Stamp `flag-YYYY-MM-DD-NNN`.
   - **Parked decision** - idea waiting for a trigger. Append to `brain/decisions-parked.md` with a Trigger to revisit line. Stamp `parked-YYYY-MM-DD-NNN`.
   - **Need / blocker** - something the user must do or decide. Add or update a row in `brain/needs-input.md` (Specific + Impact columns). Stamp `need-YYYY-MM-DD-NNN` on new entries.
   - **Preference** - the user said something about **how they want to be worked with**, not about the business. "Stop giving me three options." "I hate being asked twice." "Just tell me what you think." Append a row to the **Proposed** table in `core/working-preferences.md` - never the Active table - with the preference in their words, where it applies, today's date, and the quote as evidence. Stamp `pref-YYYY-MM-DD-NNN`. If the file does not exist, copy it from `templates/working-preferences.md` first.
   - **Client signal** - mention of a named person or company that warrants tracking. Update `context/clients.md`.
   - **Log only** - context, no action needed. Skip; the rant file itself is the record.

   For each channel: read the target file, find the highest existing `<channel>-<today>-<NNN>`, increment by 1, zero-pad to 3 digits. Track the IDs you stamp. You will cite them in the digest.

3. After distillation, mark each processed entry `processed: true` in its rants file.

4. Append a digest entry to the top of `brain/log.md`. The digest itself is a `log` entry and gets its own stamped ID. Format exactly:

   ```markdown
   ### <YYYY-MM-DD> #dream (log-YYYY-MM-DD-NNN)

   **DREAMT:** <date range>, <N> rants processed
   - <one signal in one line, max 90 chars> (#<id-of-entry-this-cites>)
   - <one signal in one line, max 90 chars> (#<id-of-entry-this-cites>)
   - <one signal in one line, max 90 chars> (#<id-of-entry-this-cites>)
   **Action:** <single recommendation, one line, max 90 chars>
   ```

   Each signal line cites the ID of the entry written in step 2 that the signal corresponds to. Example: `- Pattern: ops eating Tuesdays (#pattern-2026-05-07-001) - 3 rants this week`. The cited IDs MUST be IDs that this run actually wrote. Do not invent IDs and do not cite IDs from older entries.

   If a signal has no matching new entry (rare, when the signal is purely log-context), omit the parenthetical citation for that line.

5. Observations roll-up (optional, only when the file exists). Check for `brain/observations/<YYYY-MM-DD>.jsonl` for today's date. If the file is absent, skip this step entirely. If it exists:
   - Parse each line as JSON. Tolerate malformed lines (skip them).
   - Count total tool calls (N) and unique non-empty `file` values (M).
   - Top 3 files by count: rank `file` values by frequency, take the top 3, format as `path (count)`. When two files have the same count, break ties by alphabetical order on the file path.
   - Notable activity: scan `intent` for the case-insensitive substrings `fix`, `deploy`, `ship`, `draft`, `send`. Group hits by `file`. Take up to 3 files with the most matching observations. Same tie-break rule applies (alphabetical by file path).
   - Insert the OBSERVED block immediately after the `**Action:**` line of the digest entry you just wrote at the top of `brain/log.md`, formatted exactly:

   ```markdown
   **OBSERVED:** <N> tool calls today across <M> files
   - Most-touched files: <file1 (count1)>, <file2 (count2)>, <file3 (count3)>
   - Notable activity: <file>, <file>, <file>
   ```

   If there are fewer than 3 most-touched files, list what exists. If no files matched the notable substrings, write `Notable activity: none` on that line.

6. Output to chat: print only the 5 digest lines exactly as written to log.md. Nothing else. No preamble. No closing summary. The OBSERVED section is written to log.md but is NOT printed to chat.

## Private tag filter

Before persisting anything to a file, scan the source text for `<private>...</private>` blocks (case-insensitive). Remove every matched block (including the tags) from the text before writing. If the entire input is wrapped in `<private>`, write nothing and report "skipped - content was tagged private."

## Rules

- Hard cap on chat output: 5 lines after the heading line. If 7 patterns surfaced, pick the 3 most load-bearing. The rest are still written into `brain/patterns.md`.
- One Action only. Not a list of three.
- If zero rants are unprocessed, output exactly: `Nothing to dream. <N> rants total, all processed.`
- Do not ask the user questions inside `/dream`. If something is genuinely ambiguous, route it to `brain/needs-input.md` instead.
- **A preference is proposed, never applied.** Every other channel writes an observation the user reads later. This one would change how the OS behaves toward them, so it lands in the Proposed table and waits. A behaviour rule that appears in the file without the user ever agreeing to it is the thing they will not forgive, and `/dream` runs unattended - it is exactly where that mistake would happen. If a run proposed any preference row, the digest's Action line says so and names the count.
- Mark processed flag flips as a single edit per file, not per entry.
- Voice rules apply to all writeback (no em dashes, no banned words). The raw rant text in the rants file is exempt - it stays verbatim.
- Every ID cited in the digest must be an ID this run wrote. Never invent or fabricate IDs.
